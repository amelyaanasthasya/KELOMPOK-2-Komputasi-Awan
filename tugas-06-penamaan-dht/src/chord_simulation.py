"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)

Fungsi hashing & struktur data ring sudah disediakan.
Lengkapi TODO untuk lookup(), join(), dan leave().
"""

import hashlib

M_BITS = 8               # ruang identifier 0..255 (disederhanakan dari Chord asli yang pakai 160-bit)
RING_SIZE = 2 ** M_BITS


def hash_id(key: str) -> int:
    """Hash string (ID node atau ID kurir) ke ruang identifier 0..RING_SIZE-1."""
    digest = hashlib.sha1(key.encode()).digest()
    return int.from_bytes(digest, "big") % RING_SIZE


class ChordRing:
    def __init__(self):
        # node_id (hasil hash) -> alamat IP node tersebut
        self.nodes: dict[int, str] = {}
        # key kurir (hasil hash) -> IP kurir yang disimpan node yang bertanggung jawab
        self.data: dict[int, tuple[str, str]] = {}  # hash -> (kurir_id, ip_kurir)

    def join(self, node_name: str, node_ip: str):
        """Tambahkan node dan tampilkan perpindahan tanggung jawab."""
        node_id = hash_id(node_name)

        # Simpan kondisi ring sebelum node bergabung
        old_nodes = self.nodes.copy()

        # Tambahkan node baru ke ring
        self.nodes[node_id] = node_ip

        # Periksa apakah ada mapping yang berpindah tanggung jawab
        for key_hash, (kurir_id, ip_kurir) in self.data.items():
            old_ids = sorted(old_nodes.keys())
            old_owner = (
                next((n for n in old_ids if n >= key_hash), old_ids[0])
                if old_ids else None
            )

            new_owner = self.find_successor(key_hash)

            if old_owner != new_owner:
                print(
                    f"Mapping {kurir_id} ({ip_kurir}) "
                    f"berpindah dari node {old_owner} "
                    f"ke node {new_owner}"
                )

        print(
            f"Node '{node_name}' (id={node_id}) "
            f"bergabung, alamat {node_ip}"
        )

    def leave(self, node_name: str):
        """Keluarkan node dan tampilkan perpindahan tanggung jawab."""
        node_id = hash_id(node_name)

        # Pastikan node ada di ring
        if node_id not in self.nodes:
            print(f"Node '{node_name}' tidak ditemukan.")
            return

        # Catat mapping yang menjadi tanggung jawab node sebelum keluar
        affected_keys = [
            (key_hash, kurir_id, ip_kurir)
            for key_hash, (kurir_id, ip_kurir) in self.data.items()
            if self.find_successor(key_hash) == node_id
        ]

        # Keluarkan node dari ring
        del self.nodes[node_id]

        # Tampilkan node yang mengambil alih mapping
        if self.nodes:
            for key_hash, kurir_id, ip_kurir in affected_keys:
                new_owner = self.find_successor(key_hash)
                print(
                    f"Mapping {kurir_id} ({ip_kurir}) "
                    f"diambil alih node {new_owner}"
                )
        else:
            print("Ring kosong; tidak ada node yang mengambil alih.")

        print(f"Node '{node_name}' (id={node_id}) keluar dari ring")

    def find_successor(self, key_hash: int) -> int:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash
        (successor menurut aturan Chord). Jika tidak ada, wrap-around
        ke node dengan hash terkecil di ring (karena ring melingkar)."""

        # TODO 6
        if not self.nodes:
            raise ValueError("Ring belum memiliki node.")

        node_ids = sorted(self.nodes.keys())

        for node_id in node_ids:
            if node_id >= key_hash:
                return node_id

        return node_ids[0]

    def register_kurir(self, kurir_id: str, ip_kurir: str):

        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        
        key_hash = hash_id(kurir_id)
        # TODO 7
        if not self.nodes:
            print("Ring belum memiliki node.")
            return

        successor = self.find_successor(key_hash)
        self.data[key_hash] = (kurir_id, ip_kurir)

        print(
            f"Kurir {kurir_id} disimpan pada node {successor}"
        )

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        key_hash = hash_id(kurir_id)
        # TODO 8
        if not self.nodes:
            return None

        successor = self.find_successor(key_hash)
        record = self.data.get(key_hash)

        if record is None or record[0] != kurir_id:
            print(f"Kurir {kurir_id} tidak ditemukan.")
            return None

        print(f"Lookup {kurir_id} melalui node {successor}")
        return record[1]


def main():
    ring = ChordRing()

    # Membuat ring awal
    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-jakarta-2", "10.0.0.2")
    ring.join("node-bandung-1", "10.0.0.3")
    ring.join("node-surabaya-1", "10.0.0.4")

    # Mendaftarkan kurir
    ring.register_kurir("kurir-001", "192.168.1.10")
    ring.register_kurir("kurir-002", "192.168.1.11")
    ring.register_kurir("kurir-003", "192.168.1.12")
    ring.register_kurir("kurir-test-13", "192.168.1.13")

    print("\n--- Lookup sebelum perubahan topologi ---")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))
    print("kurir-003 ->", ring.lookup("kurir-003"))
    print("kurir-test-13 ->", ring.lookup("kurir-test-13"))

    print("\n--- Node baru bergabung ---")
    ring.join("node-medan-1", "10.0.0.5")
    print("kurir-test-13 ->", ring.lookup("kurir-test-13"))

    print("\n--- Sebuah node keluar ---")
    ring.leave("node-jakarta-1")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))
    print("kurir-test-13 ->", ring.lookup("kurir-test-13"))


if __name__ == "__main__":
    main()