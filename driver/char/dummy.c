#include <linux/init.h>
#include <linux/module.h>	/* THIS_MODULE macro */
#include <linux/fs.h>		/* VFS related */
#include <linux/errno.h>	/* error codes */
#include <linux/types.h>	/* dev_t number */
#include <linux/cdev.h>		/* char device registration */
#include <linux/uaccess.h>	/* copy_*_user functions */

/* meta information */

MODULE_LICENSE("GPL");
MODULE_AUTHOR("mfbsouza");
MODULE_DESCRIPTION("char device driver");

/* functions signature */

static int 	__init my_init (void);
static void 	__exit my_exit (void);

static int	my_open   (struct inode*, struct file*);
static int 	my_close  (struct inode*, struct file*);
static loff_t 	my_seek   (struct file*, loff_t, int);
static ssize_t 	my_read   (struct file*, char __user*, size_t, loff_t*);
static ssize_t 	my_write  (struct file*, const char __user*, size_t, loff_t*);

/* lkm entry and exit points */

module_init(my_init);
module_exit(my_exit);

/* device file operations */

static struct file_operations fops = {
	.owner = THIS_MODULE,
	.llseek = my_seek,
	.read = my_read,
	.write = my_write,
	.open = my_open,
	.release = my_close
};

/* variables for char device registration to kernel */

static dev_t my_device_nbr;
static struct class* my_class;
static struct cdev my_device;

#define DRIVER_NAME 	"my_driver"
#define FILE_NAME 	"mydev"
#define DRIVER_CLASS 	"MyModuleClass"

/* fake device */

#define BUFFER_LEN 255
static char device_mem[BUFFER_LEN];
static int buffer_index = 0;

/* functions implementation */

static int __init my_init(void)
{
	printk("my_driver: loaded to the kernel\n");

	/* 1. request the kernel for a device number */

	if (alloc_chrdev_region(&my_device_nbr, 0, 1, DRIVER_NAME) < 0) {
		printk("my_driver: device number could not be allocated!\n");
		return -EAGAIN;
	}
	printk("my_driver: device number %d was registered!\n", MAJOR(my_device_nbr));

	/* 2. create class : appears at /sys/class */

	if ((my_class = class_create(THIS_MODULE, DRIVER_CLASS)) == NULL) {
		printk("my_driver: device class count not be created!\n");
		goto ClassError;
	}

	/* 3. associate the cdev with a set of file operations */
	
	cdev_init(&my_device, &fops);

	/* 4. create the device node */

	if (device_create(my_class, NULL, my_device_nbr, NULL, FILE_NAME) == NULL) {
		printk("my_driver: can not create device file!\n");
		goto FileError;
	}

	/* 5. now make the device live for the users to access */
	
	if (cdev_add(&my_device, my_device_nbr, 1) == -1){
		printk("my_driver: registering of device to kernel failed!\n");
		goto AddError;
	}

	return 0;

AddError:
	device_destroy(my_class, my_device_nbr);
FileError:
	class_destroy(my_class);
ClassError:
	unregister_chrdev(my_device_nbr, DRIVER_NAME);
	return -EAGAIN;
}

static void __exit my_exit(void)
{
	cdev_del(&my_device);
	device_destroy(my_class, my_device_nbr);
	class_destroy(my_class);
	unregister_chrdev(my_device_nbr, DRIVER_NAME);
	printk("my_driver: goodbye kernel!\n");
}

static int my_open(struct inode* inode, struct file* filp)
{
	printk("my_driver: open was called\n");
	return 0;
}

static int my_close(struct inode* inode, struct file* filp)
{
	printk("my_driver: close was called\n");
	return 0;
}

static loff_t my_seek(struct file* filp, loff_t off, int whence)
{
	loff_t new_pos;

	switch(whence) {
	case 0: /* SEEK_SET */
		new_pos = off;
		break;
	case 1: /* SEEK_CUR */
		new_pos = filp->f_pos + off;
		break;
	case 2: /* SEEK_END */
		new_pos = BUFFER_LEN + off; //TODO: this might be wrong
		break;
	default: /* can't happen */
		new_pos = -EINVAL;
		goto SeekOut;
	}
	filp->f_pos = new_pos;

SeekOut:
	return new_pos;

}

static ssize_t my_read(struct file* filp, char __user* buf, size_t count, loff_t* f_pos)
{
	ssize_t retval = 0;
	int to_cpy = 0;

	/* check if there is something to read */
	if (*f_pos >= buffer_index) {
		printk("my_driver: trying to read a empty buffer region");
		goto ReadOut;
	}

	/* get amount of bytes to copy to user */
	to_cpy = (count <= buffer_index - *f_pos) ? count : buffer_index - *f_pos;

	/* copy data to user */
	retval = to_cpy - copy_to_user(buf, device_mem + *f_pos, to_cpy);

	/* update the file position */
	*f_pos += retval;

ReadOut:
	return retval;
}

static ssize_t my_write(struct file* filp, const char __user* buf, size_t count, loff_t* f_pos)
{
	ssize_t retval = 0;
	int to_cpy = 0;

	/* check if the buffer is full */
	if (buffer_index >= BUFFER_LEN) {
		printk("my_driver: trying to write in a full buffer");
		goto WriteOut;
	}

	/* get amount of data to copy */
	to_cpy = (count <= BUFFER_LEN - buffer_index) ? count : BUFFER_LEN - buffer_index;

	/* copy data from user */
	retval = to_cpy - copy_from_user(device_mem + buffer_index, buf, to_cpy);

	/* update buffer_index position */
	buffer_index += retval;

WriteOut:
	return retval;
}
