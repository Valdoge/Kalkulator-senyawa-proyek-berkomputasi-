#NIM/Nama:16025053/Rizky Rivaldo
#Tanggal: 2 Oktober 2025
#Deskripsi

n=int(input("Masukkan jumlah lembar saham yang dibeli:"))
harga_beli=int(input("Masukkan harga per lembar saham saat beli:"))
harga_jual=int(input("Masukkan harga per lembar saham saat jual:"))
biaya_beli=float(input("Masukkan biaya beli(persen):"))
biaya_jual=float(input("Masukkan biaya jual(persen):"))

total_beli=n*harga_beli
biaya_beli_modal=total_beli*(biaya_beli/100)
modal=total_beli+biaya_beli_modal

total_jual=n*harga_jual
biaya_jual_total=total_jual*(biaya_jual/100)
hasil_jual=total_jual+biaya_jual_total

keuntungan=hasil_jual-modal
ROI=(keuntungan/modal)*100

print("Investor tersebut mendapatkan keuntungan/kerugian bersih sebesar:", keuntungan, "dengan ROI sebesar:", ROI,)