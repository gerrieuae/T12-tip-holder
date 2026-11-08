# Turn a 3MF over (180 deg about X) and drop it to Z 0, so the lid prints top face down.
import zipfile,re,sys,shutil
src=sys.argv[1]; tmp=src+'.tmp'
zin=zipfile.ZipFile(src); n=[x for x in zin.namelist() if x.endswith('.model')][0]; s=zin.read(n).decode()
V=[(float(y),float(z)) for y,z in re.findall(r'<vertex [^>]*y="([-\d.e]+)" z="([-\d.e]+)"',s)]
ymax=max(v[0] for v in V); zmax=max(v[1] for v in V)
s=re.sub(r'(<vertex [^>]*y=")([-\d.e]+)(" z=")([-\d.e]+)"',lambda m:'%s%.6f%s%.6f"'%(m.group(1),ymax-float(m.group(2)),m.group(3),zmax-float(m.group(4))),s)
zout=zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED)
for it in zin.infolist(): zout.writestr(it, s if it.filename==n else zin.read(it.filename))
zout.close(); zin.close(); shutil.move(tmp,src); print('flipped',src)
