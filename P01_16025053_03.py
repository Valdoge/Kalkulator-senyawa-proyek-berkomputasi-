#NIM/Nama:16025053/Rizky Rivaldo
#Tanggal: 2 Oktober 2025
#Deskripsi: 

V=int(input("Masukkan jumlah pengunjung per hari:"))
C=float(input("Masukkan konversi pengunjung (persen):"))
T=int(input("Masukkan rata rata transaksi per pelanggan(Rp):"))
Iklan=int(input("Masukkan biaya iklan per pengunjung:"))
Pembayaran=float(input("Masukkan biaya pembayaran (persen):"))
Operasional=int(input("Masukkan biaya operasional tetap:"))
Variabel=float(input("Masukkan biaya variabel (persen):"))
Target=float(input("Masukkan target margin (persen)):"))

pelanggan=V*(C/100)
revenue=pelanggan*T

total_iklan=V*Iklan
biaya_pembayaran=(Pembayaran/100)*revenue
biaya_variabel=(Variabel/100)*revenue

total_biaya=total_iklan+biaya_pembayaran+biaya_variabel+Operasional
profit=revenue-total_biaya

margin=(profit/revenue)*100
target_profit=revenue*(Target/100)
selisih=profit-target_profit

status=int(margin >= target_profit)
print("status target margin tercapai", status, "dengan selisih profit sebesar", selisih)