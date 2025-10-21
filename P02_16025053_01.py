#NIM?Nama: 16025053/Rizky Rivaldo
#Tanggal: 16 Oktober 2025
#Deskripsi: Menentukan apakah dua orang bisa meeting pada hari yang sama berdasarkan range hari kosong milik mereka dengan menggunakan array dan loop

#input range hari kosong
Sal_awal=int(input("Masukkan jadwal kosong Nona Sal (range awal):"))
Sal_akhir=int(input("Masukkan jadwal kosong Nona Sal (range akhir):"))
Deb_awal=int(input("Masukkan jadwal kosong Nona Deb (range awal):"))
Deb_akhir=int(input("Masukkan jadwal kosong Nona Deb (range akhir):"))

#data hari
hari=[1,2,3,4,5,6,7]
hari_Sal=[]
hari_Deb=[]

#pengisian data hari sal dan deb
for h in hari:
    if Sal_awal<=h<=Sal_akhir:
        hari_Sal.append(h)
for h in hari:
    if Deb_awal<=h<=Deb_akhir:
        hari_Deb.append(h)

#mencari irisan hari
Hari_meeting=[]
for h in hari_Sal:
    if h in hari_Deb:
        Hari_meeting.append(h)

#Hasil
if len(Hari_meeting)==0:
    print("Meeting tidak dapat dilaksanakan")
elif len(Hari_meeting)==1:
    print(f" Meeting dapat dilaksanakan pada hari {Hari_meeting[0]}")
else:
    print(f"Meeting dapat dilaksanakan pada hari {Hari_meeting[0]} hingga hari {Hari_meeting[-1]}")