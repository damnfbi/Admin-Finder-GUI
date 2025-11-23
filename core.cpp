#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <iomanip>

constexpr size_t SECTOR_SIZE = 512; 
struct FileSignature {
    std::string name;
    std::vector<unsigned char> header;
};
class DiskAccess {
private:
    std::fstream raw_disk_simulator; 
public:
    DiskAccess(const std::string& simulated_file_path) {
        raw_disk_simulator.open(simulated_file_path, std::ios::binary | std::ios::in);
        if (!raw_disk_simulator.is_open()) {
            std::cerr << "ERROR: Could not open simulated disk file.\n";
        }
    }
    ~DiskAccess() {
        if (raw_disk_simulator.is_open()) {
            raw_disk_simulator.close();
        }
    }
    bool readSector(long long sector_number, std::vector<unsigned char>& buffer) {
        if (!raw_disk_simulator.is_open()) return false;
        buffer.resize(SECTOR_SIZE);
        raw_disk_simulator.seekg(sector_number * SECTOR_SIZE);
        raw_disk_simulator.read(reinterpret_cast<char*>(buffer.data()), SECTOR_SIZE);
        return raw_disk_simulator.gcount() == SECTOR_SIZE;
    }  
};
void scan_and_recover(DiskAccess& disk) {
    std::vector<FileSignature> signatures = {
        {"JPEG", {0xFF, 0xD8, 0xFF}}, 
        {"PDF", {0x25, 0x50, 0x44, 0x46, 0x2D}}, 
        {"PNG", {0x89, 0x50, 0x4E, 0x47}}
    };

    std::vector<unsigned char> sector_buffer(SECTOR_SIZE);
    long long current_sector = 0;
    int files_found = 0;

    std::cout << "Starting simulated raw disk scan...\n";

    while (disk.readSector(current_sector, sector_buffer)) {
        
        for (const auto& sig : signatures) {
            
            if (sector_buffer.size() >= sig.header.size() &&
                std::equal(sig.header.begin(), sig.header.end(), sector_buffer.begin())) 
            {
                files_found++;
                std::cout << "--> FOUND " << sig.name << " header at Sector: " << current_sector << "\n";
            }
        }
        current_sector++;
    }

    std::cout << "\nScan finished. Total potential files detected: " << files_found << "\n";
}

int main() {
    std::cout << "--- WARNING: This program is conceptual and requires a 'raw_disk_image.dat' file. ---\n\n";

    DiskAccess disk("raw_disk_image.dat");

    scan_and_recover(disk);

    return 0;
}