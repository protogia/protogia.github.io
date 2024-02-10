---
title: 'Beautyboot'
date: '2024-01-31T06:06:35+01:00'
author: 'Giancarlo Rizzo'
draft: false
categories: [linux]
color: '#f99157'
---

# Prologue

Since i decided to upgrade to [Ubuntu 23.10 (Mantic)](https://releases.ubuntu.com/mantic/) i had to spend some time to configure my environment, because this release came with a lot of changes. One that is not realy effecting my work but was annoying to watch, was the bootup-screen-design. The default Ubuntu-logo is printed to the bottom of the screen in a way it seems like a bug or at least a provisoric solution :D

Therefore I decided to spend some time for a deep dive in the bootup-screen-process and quickly came accross [plymouth](https://linux.die.net/man/8/plymouth). 

## About plymouth

Plymouth is a software framework used in Linux distributions to manage the graphical boot process. Its primary purpose is to provide a smooth and visually pleasing transition from the system's bootloader to the login screen or desktop environment. 

Here's a general overview of how Plymouth works in the boot process:

When you power on your system, the bootloader (such as GRUB) loads the Linux kernel into memory. Plymouth becomes active early in the boot process, taking over the console and displaying a graphical splash screen.

Then as the Linux kernel initializes, Plymouth remains active, masking the potentially verbose text output that might be displayed on the screen during boot.

Once the kernel has initialized, control is passed to the init system (e.g., systemd) and other user-space processes start. Plymouth continues to run during this phase, covering the transition between kernel initialization and the login prompt or desktop environment.

Last plymouth hands over control to the display manager (e.g., GDM, LightDM) or the desktop environment, which then presents the login screen or desktop.

## Plymouth themes & configuration

To change plymouth configurations you can set one of the preeinstalled themes, install some from web or create one on your own.

To list the installed themes type:

```bash
plymouth --list
```

And to set a theme from the list type:

```bash
plymouth <themename>
plymouth -R # needs to executed after each theme-change!
```

## Create custom themes

Because none of the preeinstalled themes really catched me, I decided to create a custom theme and moreover I decided to start a theme-creator that should be able to create animations from given media-files and video-urls. Thats how I started this prohect.

It offers the ability to create animations from local video- and imagefiles and also from provided youtube-URLs within a given timerange.

To get in touch with it check out the documentation: [beautyboot](https://github.com/protogia/beautyboot)

