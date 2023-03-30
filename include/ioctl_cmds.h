#ifndef __IOCTL_CMDS_H__
#define __IOCTL_CMDS_H__

#define RD_SWITCHES   _IO('a', 'a')
#define RD_PBUTTONS   _IO('a', 'b')
#define WR_L_DISPLAY  _IO('a', 'c')
#define WR_R_DISPLAY  _IO('a', 'd')
#define WR_RED_LEDS   _IO('a', 'e')
#define WR_GREEN_LEDS _IO('a', 'f')

#endif /* __IOCTL_CMDS_H__ */
