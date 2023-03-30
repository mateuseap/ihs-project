# Useful commands

## ⚙️ Driver related commands

**REMINDER**: Most device files in a Unix-based system are stored at `/dev directory`

- **Insert a compiled module/driver to the kernel**

```bash
sudo insmod path/to/file.ko
```

- **Remove a module/driver from the kernel**
  - Usually the `module_name` is the same name as the `.ko` file inserted

```bash
sudo rmmod module_name
```

- **Change the permissions of a file or device file**
  - Permission number is a **octal number**, where 4 = read, 2 = write, 1 = execute. So 7 = 4 + 2 + 1, wich means RWX. 6 = 4 + 2, wich means RW-

```bash
sudo chmod 666 /path/to/my_device_file
```

- **List all running modules/drivers**

```bash
lsmod
```

- **List all running modules/drivers and search the output for a matching string**

```bash
lsmod | grep string
```

- **Watch the kernel output messages**

```bash
sudo dmesg
```

- **Watch the kernel output messages with more readable timestamp**

```bash
sudo dmesg -wT
```

## 📁 File related commands

- **Print out a string to the standard output (usually a terminal)**

```bash
echo "string"
```

- **Redirect the output of a command to a file using '>'**
  - The '>' operation will empty the content of the file if the file already exists

```bash
echo "string" > test
ls > test2
```

- **Redirect and append the output of a command to a file using '>>'**

```bash
echo "string" >> test
ls >> test2
```

- **Redirect the output of a command to the input of another using the '|' operator**

```bash
ls | grep Documents
```

- **Print out the full content of a file**

```bash
cat path/to/file
```

- **Print out N bytes from the beginning of a file**

```bash
head -c N path/to/file
```

- **Print out N bytes from the ending of a file**

```bash
tail -c N path/to/file
```

- **Print out N lines (until the '\n' character) from the beginning of a file**

```bash
head -n N path/to/file
```

**Print out N lines (until the '\n' character) from the ending of a file**

```bash
tail -n N path/to/file
```

- **Info about a given file**

```bash
file path/to/file
```

- **List the permission number, major and minor number, and other info about a file**

```bash
ls -la path/to/file
```
