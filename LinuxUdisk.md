
<h2>Creating a Full Install of Ubuntu 20.04 to USB that works in both BIOS and UEFI</h2>

<p>Following is based on a 16GB Target drive, adjust for larger drive.
This looks like a long list but, should take less than ten minutes to do the work.</p>

<ul>
<li>Create a Live USB or DVD using SDC, UNetbootin, mkusb, dd, etc. (See Note 1 at bottom)</li>
<li>Turn off and unplug the computer.</li>
<li>Unplug the power cable from the hard drive or unplug the hard drive from the laptop. (See Note 2 at bottom)</li>
<li>Plug the computer back in.</li>
<li>Insert and boot the Live USB or Live DVD. (Booting BIOS mode preferred).</li>
<li>Select Language and Try Ubuntu.</li>
<li>Insert the target flash drive.</li>
<li>Start GParted.</li>
<li>Unmount any mounted partitions.</li>
<li>Select Device tab and create a GPT partition table on the Target drive.</li>
<li>Create a 3GB NTFS or FAT32 partition on the right side, (optional Linux / Windows data partition, See Note 3 at bottom).</li>
<li>Create a 1MB partition on the left side, format as unformatted.</li>
<li>Create a 300MB FAT32 partition next to the 1MB partition.</li>
<li>Create a 7GB ext partition next to the 300MB partition.</li>
<li>In the remaining space create an ext4 partition, (optional for /home partition).</li>
<li>Apply All Operations.</li>
<li>Flag the 1MB partition as <strong>bios_grub</strong>.</li>
<li>Flag the 300MB partition as <strong>boot,esp</strong>.</li>
</ul>

<p><a href="https://i.stack.imgur.com/gtlMa.png" rel="nofollow noreferrer"><img src="https://i.stack.imgur.com/gtlMa.png" alt="Image of GParted"></a></p>

<ul>
<li>Start Install Ubuntu.</li>
<li>Select Language, click "Continue".</li>
<li>Select Keyboard layout, click "Continue".</li>
<li>Select Wireless network, click "Continue". (optional).</li>
<li>Select installation preference and select "Download updates while installing Ubuntu", (optional), and Select "Install third-party software ...", click "Continue". (Optional).</li>
<li>If asked about mounted partitions, select Yes, click "Continue".</li>
<li>Do not use Advanced feature disk encryption for this install method. (See Note 3 at bottom).</li>
<li>At "Installation type" select "Something else", click "Continue".</li>
<li>Under Device for boot loader installation select the target drive.</li>
<li>Select partition sdx4 and click change, select use as Ext4, select format this partition, and Mount point = "/" then OK.</li>
<li>If asked to Write previous changes... click Continue.</li>
<li>Select partition sdx5 and click change, select use as Ext4, select format this partition, and Mount point = "/home" then OK. (optional).</li>
<li>Click Install now.</li>
</ul>

<p><a href="https://i.stack.imgur.com/VjYvt.png" rel="nofollow noreferrer"><img src="https://i.stack.imgur.com/VjYvt.png" alt="Image of  Something else"></a></p>

<ul>
<li>Confirm partitions to be formatted if asked, click continue.</li>
<li>Select your location. click "Continue".</li>
<li>Insert your name, computer name, username, password and select if you want to log in automatically or require a password. - Click "Continue".</li>
<li><p>Wait until install is complete.</p></li>
<li><p>Copy the boot and the EFI folders from the Ubuntu ISO file to the boot,esp partition sdx3.</p></li>
<li><p>Copy grub.cfg from partition sdx4 /boot/grub/ to partition sdx3 /boot/grub/ overwriting the grub.cfg file.</p></li>
<li><p>Re-Install GRUB:</p>

<p><code>sudo mount /dev/sdx3 /mnt</code><br>
<code>sudo grub-install --boot-directory=/mnt/boot /dev/sdx</code></p></li>
<li><p>Turn off computer and plug in the HDD.</p></li>
<li>Replace the computer's cover.</li>
</ul>

<p>Note 1, Booting ISO Files.</p>

<ul>
<li>If you want the USB to have the ability to boot ISO files using GRUB, create the boot drive using mkusb with the usb-pack-efi option. (this replaces GRUB 2.04 with 2.02). </li>
<li>Alternatively you can put <code>rmmod tpm</code> anywhere above the first menuentry in grub.cfg.</li>
</ul>

<p>Note 2: Hard drive removal.</p>

<ul>
<li>You may omit disabling the hard drive in BIOS boot if after partitioning you choose to install grub to the root of the USB drive you are installing Ubuntu to, (ie sdx not sdx1). Be cautious, many people have overwritten the HDD MBR as default location for boot loader is sda, any items in the internal drive's grub will be added to the USB's grub. You may do an update-grub later. If you leave the HDD plugged in with UEFI install, fstab may use the HDD's UUID for /boot/efi. In this case # or delete the /boot/efi.UUID line in fstab.</li>
</ul>

<p>Note 3: Apple compatibility.</p>

<ul>
<li>If you own an Apple computer make this partition FAT32.</li>
</ul>

<p>Note 4: Encryption (optional).</p>

<ul>
<li>For method of creating Full Encryption BIOS/UEFI USB drive see: <a href="https://askubuntu.com/questions/1086309/how-to-make-bios-uefi-flash-drive-with-full-disk-encryption">How to Make BIOS/UEFI Flash Drive with Full Disk Encryption</a></li>
</ul>
    </div>
