
#NIM/Nama: 16025053/Rizky Rivaldo
#Tanggal: 16 Oktober 2025
#Deskripsi: Menentukan kedudukan dua persamaan garis y=ax+b dan y=cx+d (sejajar, berpotongan, atau tegak lurus)

#input data
jam=int(input("masukkan Jam: "))
menit=int(input("menit: "))
lampu=int(input("Banyak lampu merah: "))
Waktu_lampu=int(input("Waktu lampu merah(menit): "))
jarak=int(input("Jarak dari rumah ke GOR(km): "))
Kecepatan=int(input("Kecepatan motor(km/menit: "))

#menghitung waktu perjalanan
waktu_jalan=jarak/Kecepatan

#menghitung total waktu termasuk lampu merah
i=1
total_lampu=0
while i<=lampu:
    total_lampu=total_lampu+Waktu_lampu
    i=i+1

total_waktu=waktu_jalan+total_lampu

#Menghitung jam tiba
mulai=jam*60+menit
tiba=mulai+total_waktu
terlambat=tiba-420 #420=07:00

#menentukan hasil
if terlambat<=0:
    print("Nona Deb terlambat", int(terlambat), "menit dan ahrus melakukan hukuman 50 push up.")
elif terlambat<10:
    print("Nona Deb terlambat", int(terlambat), "menit dan harus melakukan hukuman 70 sit up.")
else:
    print("Nona Deb terlambat", int(terlambat), "menit dan harus melakukan hukuman lari 20 putaran.")