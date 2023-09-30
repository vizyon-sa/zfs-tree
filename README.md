Listing ZFS datasets as a tree
==============================

Development instructions:
-------------------------

Running `nox` will build the codebase and provide an executable in
`.nox/install/bin/zfs-tree`.

Installation instructions:
--------------------------

Running `flit install` will install an executable available on the command
line.

Usage instructions:
-------------------

The generated executable will list the zfs datasets hierarchically in a
parent/child dependency tree and will single out snapshots in boxes nested in
the tree structure.

For instance:

```console
mini-me@virtucon ~> zfs-tree
data [24.7T] → /data
├── data/videos [9.39T] → /data/videos
├── data/mugen [2.95T] → /data/mugen
├── data/esxi [51.2G] → /data/esxi
│   ├── data/esxi/lun3 [3.46M]
│   ├── data/esxi/lun2 [3.42M]
│   ├── data/esxi/lun6 [12.0M]
│   ├── data/esxi/lun1 [51.2G]
│   ├── data/esxi/lun4 [3.48M]
│   └── data/esxi/lun5 [3.85M]
├── data/backups [11.5T] → /data/backups
│   ├── data/backups/veeam [10.7T] → /data/backups/veeam
│   ├── data/backups/master [96.5G] → /data/backups/master
│   ├── data/backups/mail [5.00G] → /data/backups/mail
│   ├── data/backups/io2 [69.5G] → /data/backups/io2
│   └── data/backups/new [577G] → /data/backups/new
├── data/iso [248G] → /data/iso
├── data/tmp [584G] → /data/tmp
└── data/nfs [20.3G] → /data/nfs
aggr0 [1.97T] → /aggr0
├── aggr0/build [17.2G] → /aggr0/build
├── aggr0/vol3 [1.58T] → /aggr0/vol3
├── aggr0/webstats [61.4G] → /aggr0/webstats
└── aggr0/vol1 [323G] → /aggr0/vol1
```