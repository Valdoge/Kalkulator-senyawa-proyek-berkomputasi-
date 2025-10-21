#NIM/Nama: 16025053/Rizky Rivaldo
#Tanggal: 16 Oktober 2025
#Deskripsi: Menentukan kedudukan dua persamaan garis y=ax+b dan y=cx+d (sejajar, berpotongan, atau tegak lurus) 

#input nilai persamaan y1
a=float(input("Nilai a:"))
b=float(input("Nilai b:"))
#input nilai persamaan y2
c=float(input("Milai c:"))
d=float(input("Nilai d:"))

#Menentukan hubungan dua garis
status=""
if a==c:
    status="Sejajar"
elif a*c==-1:
    status="Tegak lurus"
else:
    status="Berpotongan"

#Jika hubungan garis tidak sejajar, cari titik potong kedua garis tersebut
if status=="Sejajar":
    print("Kedua persamaan garis saling sejajar")
#Menghitung titik potong kedua garis
else:
    status=="Berpotongan"
    x=(d-b)/(a-c)
    y=a*x+b

if status=="Tegak lurus":
    print("Kedua persamaan garis saling tegak lurus di titik (", int(x),",", int(y),")")
else:
    print("Kedua persamaan garis saling berpotongan di titik(",int(x),",", int(y),")")
