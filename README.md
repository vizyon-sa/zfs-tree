Listing ZFS datasets as a tree
==============================

Development instructions:
-------------------------

Running `nox` will build the codebase and provide an executable in
`.nox/install/bin/zfs-tree`.

Installation instructions:
--------------------------

Running `flit install` will install an executable available from the command
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

In the presence of snapshots, one get the following kind of output:

```console
├── rpool/lxd/deleted [564M]
│   ├── rpool/lxd/deleted/images [564M]
│   │   ├── ╭────────────────────────────────────────────────────────────────╮
│   │   │   │ rpool/lxd/deleted/images/3ffdb1....a05cb130bcb312.block [563M] │
│   │   │   │ └── rpool/lxd/virtual-machines/opencog.block [3.12G]           │
│   │   │   ╰────────────────────────────────────────────────────────────────╯
│   │   └── ╭────────────────────────────────────────────────────────────────╮
│   │       │ rpool/lxd/deleted/images/3ffdb12efa6a....05cb1330bcb312 [220K] │
│   │       │ └── rpool/lxd/virtual-machines/opencog [8.02M]                 │
│   │       ╰────────────────────────────────────────────────────────────────╯
│   ├── rpool/lxd/deleted/virtual-machines [192K]
│   ├── rpool/lxd/deleted/buckets [192K]
│   ├── rpool/lxd/deleted/custom [192K]
│   └── rpool/lxd/deleted/containers [192K]
```

If, for instance, (which is a situation that motivated the development of this
tool), you install a fresh ubuntu with a zfs filesystem on the root drive, and
if you subsequently install docker, you may run into weird issues of leftover
zfs snapshots that are a major pain to clean up. The zfs datasets that should
be cleaned up will appear in boxes, as above, which will ease the
identification of the zfs datasets to remove in that painstaking cleanup
process.