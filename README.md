# BG3_lsjFileUnpacker
WHY BE THE \[Wulbren Bongle\] WHO HATES THEIR \[Discount Terrorist\] LIFE WHEN YOU CAN BE A \[BIG SHOT BG3 RENDER ARTIST/MODDER!!!\] 

**Has this ever happened to you?**
You're sifting through BG3's files, only to get lost in one of the .lsj files in the mix, where there's this weird "fvec3" format next to something saying what you think is the color you're looking for. And then when you're trying to render a room for the scene you've been working on, you see something called mat4x4, and are either very confused on what a matrix is, or experiencing PTSD flashbacks to that one linear algebra class you had in college. (I know how you feel, fellow STEM majors U_U).

Well worry no longer! With a Bottle of Thren's Generic .lsj unpacker, you can have your colors in hex code, and x/y/z coordinates and angles instead of scary boxes of numbers! It also makes the files a bit easier to format, if you haven't gotten a text editor configured to parse JSON files! (And converts them into tables to get the information in a powerful, compact format).

(This is the repository for all of the stuff related to my script-project-thing. WARNING: Currently, it is literally just a Python script, so if you don't have Python, you'll need to install and run it (I promise it's not that much work if you've never used Python before).

Very barebones on the featureset so far--rename your target lsj file to "input.txt" and put it in the same folder as the unpacker script, then run it to get an output in the form of a tabbed text file. I plan to work on making the script able to batches/whole folders of files in one go soon, so this'll hopefully seem like a quaint and outdated readme instruction soon!
