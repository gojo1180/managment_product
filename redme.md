Nev Management Produc- Sistem Manajemen Inventaris

StokMaster Pro adalah aplikasi manajemen stok barang berbasis web yang dibangun menggunakan FastAPI sebagai backend dan Vue.js sebagai frontend. Aplikasi ini memungkinkan pengguna untuk mengelola stok produk baik secara manual maupun otomatis menggunakan fitur Scan QR Code.

✨ Fitur Utama

Manajemen Produk (CRUD): Tambah, Lihat, Edit, dan Hapus data produk.

Sistem Kategori Otomatis: Kategori baru akan dibuat secara otomatis jika belum ada di database.

Scan QR Code: Mencari produk secara instan menggunakan kamera perangkat atau input kode manual.

Auto-Generate QR Code: Menghasilkan kode identitas unik secara otomatis jika pengguna tidak mengisi kode manual.

Unduh QR Code: Mengonversi kode produk menjadi gambar QR Code yang siap cetak.

Real-time Stats: Ringkasan total produk, total stok, dan jumlah kategori.

🛠️ Tech Stack

Backend: FastAPI (Python 3.11+)

Database: Supabase (PostgreSQL)

Frontend: Vue.js 3 (via CDN), Tailwind CSS, Axios

Libraries:

html5-qrcode: Pemindaian QR Code via kamera browser.

qrious: Generator gambar QR Code.

lucide-react: Sistem ikon yang modern.

🚀 Cara Menjalankan Secara Lokal

1. Persiapan Database (Supabase)

Buat proyek baru di Supabase.

Jalankan perintah SQL yang tersedia di file schema.sql (jika ada) atau buat tabel categories dan products melalui SQL Editor.

Pastikan Row Level Security (RLS) dikonfigurasi agar mengizinkan akses publik (Zero Auth) sesuai kebutuhan pengembangan.

2. Setup Backend

Clone repositori ini:

git clone [https://github.com/username/stokmaster-pro.git](https://github.com/username/stokmaster-pro.git)
cd stokmaster-pro


Buat Virtual Environment dan aktifkan:

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate


Instal dependensi:

pip install -r requirements.txt


Buat file .env di root folder dan isi dengan kredensial Supabase kamu:

SUPABASE_URL=[https://your-project.supabase.co](https://your-project.supabase.co)
SUPABASE_KEY=your-anon-key


Jalankan server:

python main.py


3. Setup Frontend

Buka file index.html langsung di browser Anda. Pastikan backend sudah berjalan di http://localhost:8000.

📝 Catatan Penting

Fitur kamera (Scan QR Code) membutuhkan koneksi HTTPS jika diakses melalui perangkat mobile di luar jaringan lokal.

Pastikan izin kamera diberikan pada browser saat menggunakan fitur scan.

📄 Lisensi

Proyek ini dilisensikan di bawah MIT License.
