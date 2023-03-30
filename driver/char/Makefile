obj-m += dummy.o

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	@rm -rf *.cmd *.symvers *.ko *.mod.* *.mod *.o *.order .*.cmd
