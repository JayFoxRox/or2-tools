# or2-tools

The swiss-army-knife tool for reading OutRun 2 files is `or2.py`.
Make sure the filenames match the patterns below so the script can find the right handlers.

You can run it like this:

```
./or2.py 
```

**Warning: There is currently no way to repack these files.**


## OutRun 2 (Original Xbox)

### .CVM files

You can use [cvm_tool by roxfan and JayFoxRox](https://github.com/JayFoxRox/cvm_tool).
The resulting ISO9660 can be extracted using commonly available tools.

### .GZ files

Most game files are compressed by gzip. Some files contain extra information, such as their original uncompressed filename.

The files can be decompressed using code in `gz_extract.py`.

### CS_*_SIN files

Seem to have some indices in a single or multiple streams of 16-bit values.
Single streams might be an old version of the format or a bug in the game.

The purpose of these files is unknown.

### CS_*_BIN files

Similar to SIN files, but using 32-bit values and a single stream.

The purpose of these files is unknown.

### OBJ_*_SMT files

These files contain dynamic objects (meshes and textures).

### CS_*_SMT files

These files contain static objects for courses (meshes and textures).

### COLI files

These files contain the collision data for courses.

#### Track connections

- COLI_BK_1A_BIN.GZ = ?
- COLI_BK_1L_BIN.GZ = ?
- COLI_BK_1N_BIN.GZ = ?
- COLI_BK_1P_BIN.GZ = ?
- COLI_BK_1Q_BIN.GZ = ?
- COLI_BK_1S_BIN.GZ = ?
- COLI_BK_5A_BIN.GZ = ?
- COLI_BK_5B_BIN.GZ = ?
- COLI_BK_5C_BIN.GZ = ?
- COLI_BK_5D_BIN.GZ = ?
- COLI_BK_5E_BIN.GZ = ?

- COLI_LBK_1A_BIN.GZ = ?
- COLI_LRBK_1A_BIN.GZ = ?
- COLI_RBK_1A_BIN.GZ = ?

#### Courses

**Default Stages**

*(Stages in order of appearance and from easy to hard)*

*Stage 1*

- COLI_CS_1A_BIN.GZ / COLI_CS_1A_R_BIN.GZ = Palm Beach
- COLI_CS_1B_BIN.GZ / COLI_CS_1B_R_BIN.GZ = Palm Beach ?

*Stage 2*

- COLI_CS_2A_BIN.GZ / COLI_CS_2A_R_BIN.GZ = Deep Lake ?
- COLI_CS_3A_BIN.GZ / COLI_CS_3A_R_BIN.GZ = Alpine

*Stage 3*

- COLI_CS_4A_BIN.GZ / COLI_CS_4A_R_BIN.GZ = Castle Wall ?
- COLI_CS_4C_BIN.GZ / COLI_CS_4C_R_BIN.GZ = Coniferous Forest ?
- COLI_CS_4D_BIN.GZ / COLI_CS_4D_R_BIN.GZ = Desert ?

*Stage 4*

- COLI_CS_3C_BIN.GZ / COLI_CS_3C_R_BIN.GZ = Cloudy Highland ??
- COLI_CS_2B_BIN.GZ / COLI_CS_2B_R_BIN.GZ = Industrial Complex
- COLI_CS_3B_BIN.GZ / COLI_CS_3B_R_BIN.GZ = Snow Mountain ??
- COLI_CS_4B_BIN.GZ / COLI_CS_4B_R_BIN.GZ = Ghost Forest ??

*Stage 5*

- COLI_CS_5A_BIN.GZ / COLI_CS_5A_R_BIN.GZ = Tulip Garden ?
- COLI_CS_5F_BIN.GZ / COLI_CS_5F_R_BIN.GZ = Tulip Garden
- COLI_CS_5B_BIN.GZ / COLI_CS_5B_R_BIN.GZ = Metropolis ?
- COLI_CS_5G_BIN.GZ / COLI_CS_5G_R_BIN.GZ = Metropolis
- COLI_CS_5C_BIN.GZ / COLI_CS_5C_R_BIN.GZ = Ancient Ruins
- COLI_CS_5H_BIN.GZ / COLI_CS_5H_R_BIN.GZ = Ancient Ruins
- COLI_CS_5E_BIN.GZ / COLI_CS_5E_R_BIN.GZ = Imperial Avenue ?
- COLI_CS_5I_BIN.GZ / COLI_CS_5I_R_BIN.GZ = Imperial Avenue ?
- COLI_CS_5D_BIN.GZ / COLI_CS_5D_R_BIN.GZ = Cape Way ?
- COLI_CS_5J_BIN.GZ / COLI_CS_5J_R_BIN.GZ = Cape Way

**Bonus Stage 1 (Scud Race)**

- COLI_CS_6A_BIN.GZ = Beginner / Day (Aquarium)
- COLI_CS_6B_BIN.GZ = Beginner / Night (Airport)
- COLI_CS_6C_BIN.GZ = Medium (Ancient)
- COLI_CS_6D_BIN.GZ = Expert (Castle)

**Bonus Stage 2 (Daytona USA 2 Power Edition Challenge)**

- COLI_CS_7B_BIN.GZ = Advanced (Themepark)
- COLI_CS_7C_BIN.GZ = Expert (City)
- COLI_CS_7A_BIN.GZ = Beginner (Oval)


## OutRun 2006: Coast to Coast (Original Xbox)

This is about the original Xbox version of the game.

### .SZ files

Same as "OutRun 2 (Original Xbox) / *.GZ files".

### OBJ_*_PMT files

Similar to "OutRun 2 (Original Xbox) / OBJ_*_SMT files".

### CS_*_PMT files

Similar to "OutRun 2 (Original Xbox) / OBJ_*_SMT files".


## License

**(C)2020 Jannik Vogel**

**Warning: As the OutRun games are copyrighted, extracted information (or derivatives thereof) can not be redistributed.**
