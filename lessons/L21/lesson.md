---
id: L21
title: Bản đồ ổ đĩa và bộ nhớ máy tính: HDD, SSD, RAM, HBM và hơn thế nữa
topic: ky-thuat
date: 2026-11-05
---
# Bản đồ ổ đĩa và bộ nhớ máy tính: HDD, SSD, RAM, HBM và hơn thế nữa

Câu hỏi của bài: máy tính có HDD, SSD, RAM, HBM và nhiều loại khác; loại nào thật sự giữ dữ liệu, loại nào chỉ là mặt bàn làm việc, vì sao loại này nhanh, loại kia rẻ, và khi nào nên chọn loại nào?

Bài viết cho kỹ sư và người đi làm **không chuyên phần cứng**. Thuật ngữ kỹ thuật kèm tiếng Anh ở lần đầu. Câu có `[Sn]` là điều nguồn đã nói; "Ví dụ của người viết" là ví von để dễ nhớ; "Suy luận của người viết" và "tự tính" là phần người viết rút ra, không phải lời của nguồn. **Mọi số liệu là số tham khảo, tính đến 11/2026**; giá thay đổi rất nhanh.

## Bộ nhớ và lưu trữ: bức tranh chung

Máy tính có hai nhóm thành phần hay bị gọi chung là "bộ nhớ". **Bộ nhớ** (memory), như RAM, là nơi CPU làm việc trực tiếp: rất nhanh nhưng mất dữ liệu khi tắt điện, nên gọi là **bay hơi** (volatile). **Lưu trữ** (storage), như HDD, SSD, băng từ, là nơi cất dữ liệu lâu dài: chậm hơn nhưng giữ dữ liệu khi không có điện, nên gọi là **không bay hơi** (non-volatile). Ổ SSD là loại lưu trữ dựa trên bộ nhớ flash không bay hơi, thường là NAND flash [S4]. RAM và HBM thuộc nhóm bộ nhớ chứ không phải ổ đĩa lưu trữ: tắt máy là trống.

Ví dụ của người viết: CPU là người làm việc. RAM là mặt bàn làm việc: với tay là lấy được ngay nhưng bàn nhỏ, và cuối ngày bàn được dọn sạch. SSD là tủ hồ sơ cạnh bàn: lấy nhanh vừa phải, giữ lâu dài. HDD và băng từ là kho lưu trữ: chứa rất nhiều, rẻ, nhưng đi lấy mất thời gian.

Các loại bộ nhớ xếp thành một **kim tự tháp**: càng gần CPU càng nhanh, nhỏ và đắt trên mỗi GB; càng xa càng chậm, lớn và rẻ. Từ trên xuống: thanh ghi (register) trong CPU, **cache SRAM** trong CPU, RAM (DRAM), SSD, HDD, băng từ (tape). Mức độ trễ và dung lượng dưới đây là bậc độ lớn thường gặp, thuộc kiến thức nền của người viết, không kèm nguồn riêng: thanh ghi dưới 1 ns; cache khoảng 1 đến 10 ns; DRAM khoảng 50 đến 100 ns; SSD khoảng 10 đến 100 µs; HDD khoảng 5 đến 15 ms; băng từ cần giây đến phút để nạp và dò đến đoạn băng cần đọc. Giá bán lẻ tham khảo tháng 11/2026: bộ DDR5 32 GB khoảng 429 đến 600 USD, tức khoảng 13 đến 19 USD mỗi GB [S34]; ổ HDD dung lượng lớn khoảng 22 đến 40 USD mỗi TB, tức khoảng 0,02 đến 0,04 USD mỗi GB [S35]. Trong một mẫu 130 ổ SSD mới trên trang theo dõi giá, người viết tự tính giá trên mỗi TB từ khoảng 82 đến 760 USD, trung vị khoảng 190 USD, tức khoảng 0,08 đến 0,19 USD mỗi GB cho phần lớn ổ phổ thông [S36]. Giá của cả DRAM và flash đang tăng mạnh vì nhu cầu AI [S34][S36].

Trên bo mạch chủ, mỗi thành phần có một chỗ riêng: CPU nằm trong socket và mang theo cache; RAM cắm vào các khe DIMM; SSD NVMe cắm vào khe M.2 hoặc các khe chuyên dụng khác; HDD và SSD SATA nối bằng cáp SATA; card đồ họa hoặc GPU cho AI cắm vào khe PCIe và mang theo bộ nhớ riêng, GDDR hoặc HBM. Bài này đi qua từng loại theo thứ tự: HDD, SSD, các loại lưu trữ khác, RAM, HBM và CXL, rồi so sánh và hướng dẫn chọn.

## HDD: ổ đĩa cơ

**HDD** (hard disk drive, ổ đĩa cứng) lưu dữ liệu bằng từ tính trên các đĩa quay. Một ổ điển hình gồm **trục quay** (spindle) giữ các **đĩa** (platter) hình tròn phủ vật liệu từ; các **đầu đọc ghi** (head) gắn trên một **cần di chuyển** (actuator arm) đọc và ghi dữ liệu lên bề mặt đĩa khi đĩa quay ngang qua [S1]. Phía dưới còn có **bảng mạch điều khiển** (PCB) nối ổ với máy tính. Ví dụ của người viết: HDD giống một đĩa nhạc có kim đọc, nhưng kim bay sát mặt đĩa rất gần mà không chạm vào.

Ổ có hai kích thước phổ biến: 3,5 inch cho máy bàn và NAS, 2,5 inch cho laptop. Ổ 2,5 inch nhỏ và mỏng hơn ổ 3,5 inch, nhưng cùng dùng giắc SATA để nối dữ liệu và nguồn [S1][S9].

Vì sao HDD chậm? Mỗi lần truy cập, đầu đọc phải di chuyển đến đúng track (thời gian dò, seek time), rồi chờ đĩa quay đến đúng vị trí (độ trễ quay, rotational latency) [S1]. Đa số HDD phổ thông quay 5.400 hoặc 7.200 vòng mỗi phút [S1]. Người viết tự tính: độ trễ quay trung bình bằng nửa vòng quay, tức 60 / 5.400 / 2 khoảng 5,56 ms ở 5.400 vòng/phút và 60 / 7.200 / 2 khoảng 4,17 ms ở 7.200 vòng/phút. Một SSD không có bộ phận chuyển động nên bỏ qua cả hai khoản chờ này.

Hai kiểu ghi dữ liệu trên đĩa cần phân biệt. **CMR** (conventional magnetic recording, ghi từ thông thường) ghi các track không chồng lên nhau. **SMR** (shingled magnetic recording, ghi từ xếp chồng) ghi track mới chồng lên một phần track trước như ngói trên mái nhà, nên chứa được nhiều dữ liệu hơn trên cùng diện tích [S2]. Cái giá: khi ghi một track, track kề bên cũng bị ghi đè; nếu track kề đang chứa dữ liệu hợp lệ thì phải ghi lại cả chuỗi, nên một lệnh ghi có thể kéo theo nhiều lệnh ghi lại [S2]. Suy luận của người viết: ổ SMR hợp với dữ liệu ghi một lần rồi ít sửa như backup hoặc lưu trữ, còn ổ CMR hợp với việc ghi ngẫu nhiên thường xuyên như NAS đang chạy nhiều tác vụ.

Dung lượng HDD vẫn tăng. Wikipedia ghi HDD đến 36 TB đã có mặt năm 2025 [S4]. Seagate cho biết đã giao một số lượng giới hạn ổ 40 TB dùng công nghệ ghi bằng nhiệt HAMR (heat-assisted magnetic recording), đạt 4 TB mỗi đĩa với mười đĩa, và dự kiến sản xuất quy mô lớn trong nửa đầu năm 2026 [S3]. Một số ổ dùng khí heli bên trong thay cho không khí; hãng HGST (nay thuộc Western Digital) chọn hướng này vì ít nhiễu loạn hơn nên có thể ghi dày hơn [S1].

Ưu điểm của HDD: rẻ hơn SSD nhiều trên mỗi TB và có dung lượng rất lớn [S35]. Nhược điểm: chậm khi truy cập ngẫu nhiên, ồn, nhạy với va đập vì có bộ phận chuyển động. Ứng dụng điển hình: NAS, camera giám sát, lưu trữ lớn trong trung tâm dữ liệu, backup.

## SSD: nguyên lý và cấu tạo

**SSD** (solid-state drive, ổ thể rắn) là thiết bị lưu trữ không có bộ phận chuyển động; nó lưu dữ liệu trong các ô nhớ của bộ nhớ không bay hơi, thường là NAND flash [S4]. **NAND flash** lưu một bit bằng cách giữ hoặc bỏ điện tích trong một ô nhớ (cell) có thể giữ điện ngay cả khi mất điện nguồn [S6]. Ví dụ của người viết: SSD như tủ hồ sơ nhiều ngăn kéo; mở ngăn nào cũng mất thời gian như nhau, không phải chờ kim đi tới.

Cấu tạo bên trong một SSD gồm bốn phần chính. Một là các **chip NAND** chứa dữ liệu. Hai là **bộ điều khiển** (controller), chip trung tâm điều phối việc đọc, ghi, xóa, sửa lỗi và dàn đều số lần ghi giữa các ô (wear leveling) [S4]. Ba là **bộ nhớ đệm DRAM** (DRAM cache) giữ bảng ánh xạ địa chỉ; nhiều ổ giá rẻ bỏ chip này. Bốn là **bảng mạch** (PCB) và đầu nối. Với ổ NVMe không có DRAM, công nghệ **HMB** (host memory buffer) cho phép SSD mượn một phần RAM của máy làm bộ đệm, giảm giá thành mà vẫn giữ hiệu năng đọc khá tốt [S4]. Ngoài ra, nhiều SSD dùng một vùng **SLC cache**: dữ liệu được ghi nhanh vào vùng tế bào chạy ở chế độ một bit, rồi mới chuyển sang vùng chứa nhiều bit hơn nhưng chậm hơn [S4]. Đó là lý do một SSD có thể ghi rất nhanh lúc đầu rồi chậm lại khi ghi liên tục một lượng lớn dữ liệu (suy luận của người viết từ cơ chế này).

Hình dáng bên ngoài của SSD rất đa dạng. Với máy tính cá nhân: **SATA 2,5 inch** (cùng cỡ với ổ laptop), **mSATA** (thẻ nhỏ, đời cũ), và **M.2**. M.2 là thẻ dài cắm thẳng vào khe trên bo mạch; số "2280" trong tên là quy ước kích thước, nghĩa là rộng 22 mm và dài 80 mm (kiến thức nền của người viết). mSATA, M.2, U.2 và EDSFF đều là các hình dáng mới hơn so với kiểu ổ 2,5 inch thừa hưởng từ HDD [S4]. Với máy chủ: **U.2** (2,5 inch, có biến thể U.3), các cỡ **EDSFF** như E1.S, E3.S và E3.L, và **thẻ cắm PCIe** (add-in card) [S10]. Ổ 245 TB của Micron có hai dạng U.2 15 mm và E3.L [S13]. EDSFF (enterprise and data center standard form factor) hot-swap được và tối ưu làm mát cho máy chủ, trong khi M.2 không được thiết kế để cắm nóng (theo mô tả chung của người viết về cách dùng, không kèm nguồn riêng).

## SSD: loại cell và 3D NAND

Một ô nhớ NAND lưu được nhiều hơn một bit bằng cách phân biệt nhiều mức điện tích. Tên các loại: **SLC** (single-level cell) 1 bit mỗi ô, **MLC** 2 bit, **TLC** 3 bit, **QLC** 4 bit, **PLC** 5 bit [S5]. Người viết tự tính: n bit cần phân biệt 2 mũ n mức, tức 2, 4, 8, 16 và 32 mức. Càng nhiều mức, các mức càng sát nhau nên ghi chậm hơn, dễ sai hơn và mòn nhanh hơn, đổi lại rẻ hơn trên mỗi GB vì cùng một ô chứa được nhiều bit hơn [S5].

Tuổi thọ tính theo số **chu kỳ ghi xóa** (P/E cycles, program/erase cycles). Một bảng tổng hợp nêu SLC khoảng 50.000 đến 100.000 chu kỳ, MLC khoảng 10.000, TLC khoảng 3.000 [S7]; QLC thấp hơn nữa và các nguồn còn lệch nhau, nên bài chỉ nói "khoảng một nghìn hoặc thấp hơn" và không gán con số chắc chắn. Mức tốc độ và giá: SLC nhanh nhất, bền nhất và đắt nhất; QLC chậm nhất, ít bền nhất và rẻ nhất; TLC là điểm cân bằng phổ biến cho ổ phổ thông (suy luận của người viết, khớp với nguồn về xu hướng "càng nhiều bit càng rẻ và càng chậm" [S5][S7]).

**3D NAND** (cũng gọi V-NAND) giải bài toán thu nhỏ: thay vì dàn các ô trên một lớp phẳng ngày càng nhỏ, người ta **xếp các lớp ô lên cao** và đục lỗ thẳng đứng xuyên qua nhiều lớp [S6]. Số tầng đã vượt 300: SK hynix được báo cáo nhắm đến NAND QLC 321 tầng vào nửa cuối 2026 [S14]. Con số của các hãng khác chưa kiểm được nguồn nên bài không nêu.

## SSD: giao tiếp, tốc độ và độ bền

Có hai cách nối SSD với máy. **SATA** là giao diện thiết kế từ thời HDD; bản SATA 3.0 chạy 6 Gbit/s, tức tối đa 600 MB/s [S9]. **NVMe** (non-volatile memory express) là giao thức dành cho bộ nhớ flash, đi qua đường **PCIe**; so với giao thức AHCI cũ, nó có nhiều hàng đợi lệnh dài và độ trễ thấp hơn [S8]. Ví dụ của người viết: SATA như đường quốc lộ một làn đi qua nhiều trạm thu phí; NVMe như đường cao tốc nhiều làn nối thẳng từ CPU.

**PCIe** nâng tốc độ mỗi thế hệ gấp đôi. PCIe 7.0 chạy 128 GT/s mỗi làn mỗi chiều, gấp đôi PCIe 6.0 và gấp bốn PCIe 5.0 [S11]. Người viết tự tính từ tỷ lệ này: PCIe 6.0 là 64 GT/s và PCIe 5.0 là 32 GT/s mỗi làn; với bốn làn (x4), băng thông tối đa mỗi chiều khoảng 4, 8, 16 và 32 GB/s cho PCIe 3.0, 4.0, 5.0 và 6.0 (đổi GT/s sang GB/s bằng cách chia 8 rồi nhân bốn làn), chưa trừ chi phí giao thức; ổ thực tế luôn thấp hơn. Micron 6600 ION là ổ doanh nghiệp PCIe 5.0 x4 công bố đọc tuần tự 13.700 MB/s [S13], tức khoảng 23 lần giới hạn 600 MB/s của SATA (tự tính). Micron 9650 dùng giao diện PCIe 6.0 x4 và NVMe 2.0, công bố đọc tuần tự đến 28.000 MB/s và ghi 14.000 MB/s, là SSD PCIe 6.0 đầu tiên vào sản xuất hàng loạt, dành cho trung tâm dữ liệu [S12]. Bài chưa có nguồn cho ổ PCIe 6.0 dành cho người dùng cá nhân.

**Độ bền** của SSD thường ghi trên bảng thông số dưới hai dạng: **TBW** (terabytes written, tổng số terabyte được phép ghi) hoặc **DWPD** (drive writes per day, số lần ghi đầy ổ mỗi ngày) [S4]. Ví dụ trong nguồn: Samsung 970 EVO 1 TB có độ bền 600 TBW; TBW đo lượng dữ liệu mà máy chủ ghi vào ổ, không quy đổi thẳng ra số chu kỳ ghi xóa của ô nhớ, vì bộ điều khiển có thể ghi vào NAND nhiều hơn lượng dữ liệu máy chủ gửi (khuếch đại ghi, write amplification) [S4]. Người viết tự tính với giả định bảo hành 5 năm: 600 TB chia cho (1 TB nhân 365 ngày nhân 5 năm) khoảng 0,33 lần ghi đầy ổ mỗi ngày, tức DWPD khoảng 0,33.

Cuối cùng là khác biệt giữa **ổ người dùng** (consumer) và **ổ doanh nghiệp** (enterprise, datacenter). Người viết tóm theo hướng sử dụng thực tế: ổ doanh nghiệp thường có độ bền DWPD cao hơn, hiệu năng ổn định khi tải nặng, nhiều dạng cắm nóng như U.2 hay EDSFF [S10], và dung lượng cực lớn: Micron 6600 ION đạt 245,76 TB bằng NAND QLC, giao diện PCIe 5.0 x4, bắt đầu giao ngày 5/5/2026 [S13]. Các tính năng khác như bảo vệ dữ liệu khi mất điện đột ngột là kiến thức nền của người viết, không kèm nguồn riêng.

## Các loại lưu trữ khác

**USB flash drive** (ổ USB), **thẻ SD và microSD** đều dùng NAND flash, loại bộ nhớ có mặt chủ yếu trong thẻ nhớ, ổ USB, SSD và điện thoại; một thiết bị flash gồm một hay nhiều chip nhớ cùng một chip điều khiển riêng [S15]. Bên trong một ổ USB điển hình có đầu nối USB-A, một chip điều khiển mass storage, chip nhớ flash, thạch anh tạo xung nhịp, và tùy loại có đèn LED hay công tắc chống ghi [S33]. Về bản chất ổ USB là một "SSD nhỏ" cắm cổng USB. Chuẩn thẻ SDUC hỗ trợ thẻ đến 128 TiB [S15]; thẻ thực tế nhỏ hơn rất nhiều.

**eMMC** (embedded MMC) là gói bộ nhớ NAND flash nhúng hàn thẳng lên bo mạch của thiết bị, nên không tháo ra được; từ năm 2007 Toshiba đã làm gói eMMC xếp chồng nhiều die [S15]. **UFS** (universal flash storage) là thế hệ kế tiếp cho điện thoại, ô tô và thiết bị nhúng; JEDEC công bố UFS 5.0 đạt tuần tự đến 10,8 GB/s, gấp đôi UFS 4.1 [S16].

**Ổ quang** đọc dữ liệu bằng tia laser trên đĩa nhựa có các hố nhỏ (pit). CD chứa khoảng 700 MiB dữ liệu (80 phút âm thanh) [S17]. DVD và Blu-ray dùng laser bước sóng ngắn hơn nên chứa nhiều hơn rất nhiều (kiến thức nền của người viết). Ổ quang nay chủ yếu để phát phim và lưu trữ đặc thù.

**Băng từ LTO** (Linear Tape-Open) là cuộn băng từ trong hộp nhựa, đọc bằng ổ băng. LTO-10 có hộp 40 TB dung lượng gốc (native), tương đương 100 TB khi nén; Fujifilm bắt đầu giao hàng từ tháng 1 năm 2026 [S19]. LTO-9 có 18 TB gốc [S18]. Băng từ chậm khi truy cập ngẫu nhiên nhưng rất hợp lưu trữ dài hạn và backup.

**Optane** (3D XPoint) là loại bộ nhớ không bay hơi của Intel và Micron, đọc ghi theo byte và độ trễ ghi thấp [S20]. Intel công bố ngừng kinh doanh Optane và ghi giảm giá trị tồn kho 559 triệu USD; CEO Intel nêu lý do là xu hướng chuyển sang kiến trúc dựa trên CXL [S21]. **Đĩa mềm** (floppy) là bộ nhớ từ tính tháo rời, dung lượng chỉ vài MB, nay chỉ còn ý nghĩa lịch sử (kiến thức nền của người viết).

## RAM: SRAM, DRAM và các module

Bộ nhớ truy cập ngẫu nhiên có hai họ chính. **SRAM** (static RAM) lưu mỗi bit trong một ô thường gồm sáu transistor [S22]: nhanh, không cần làm tươi, nhưng tốn diện tích và đắt, nên dùng làm cache trong CPU. **DRAM** (dynamic RAM) lưu mỗi bit bằng một transistor và một tụ điện; điện tích trong tụ rò dần nên phải được **làm tươi** (refresh) liên tục [S23]. DRAM gọn và rẻ hơn trên mỗi bit nên dùng làm RAM chính. Cả hai mất dữ liệu khi tắt điện.

RAM cắm vào máy qua các **module DIMM** (dual in-line memory module): thanh dài cho máy bàn và máy chủ; **SO-DIMM** là bản nhỏ cho laptop và mini PC [S25]. Mỗi thế hệ DIMM có rãnh khía (notch) ở vị trí khác nhau nên không cắm nhầm thế hệ [S25]. **ECC** (error-correcting code) là bộ nhớ có thêm bit kiểm tra để phát hiện và sửa lỗi bit; bộ nhớ **registered** (RDIMM) thêm mạch đệm giữa module và bộ điều khiển, dùng nhiều trong máy chủ [S26].

**DDR5** là thế hệ DDR hiện hành: điện áp danh định 1,1 V với bộ điều chỉnh điện áp ngay trên module, có ECC trên chip (on-die ECC) và chia mỗi module thành các kênh con độc lập [S24]. Giá DDR5 đang rất cao: bộ 32 GB khoảng 429 đến 600 USD, trong khi trước đợt thiếu hụt khoảng 95 USD; DDR4 rẻ hơn khoảng 56% trên mỗi GB [S34]. **LPDDR** là biến thể tiết kiệm điện dùng trong điện thoại và laptop mỏng; **GDDR** là biến thể thiết kế riêng cho card đồ họa, ưu tiên băng thông [S27]. Thông số chi tiết của LPDDR6 và GDDR7 chưa kiểm được nguồn nên bài không nêu số.

## HBM và CXL

GPU cho AI cần đọc dữ liệu nhanh hơn rất nhiều so với RAM thường cho phép. **HBM** (high bandwidth memory, bộ nhớ băng thông cao) giải quyết bằng cách **xếp chồng nhiều die DRAM** thành một tòa nhà, đặt ngay sát bộ xử lý [S28]. Ví dụ của người viết: thay vì dãy nhà trệt trải xa, HBM là tòa nhà nhiều tầng ngay cạnh GPU: lối đi ngắn, nhiều làn.

Cấu tạo: 4, 8, 12 hoặc 16 die DRAM xếp trên một **die logic đáy** (base die); các die nối với nhau bằng **TSV** (through-silicon via, lỗ xuyên silicon) cùng các chấm nối nhỏ; cả stack đặt cạnh GPU trên một **interposer** (tấm silicon nối) [S28]. Mỗi stack có bus 1024 bit, riêng HBM4 lên đến 2048 bit [S28]. Nhờ đường truyền ngắn và rất rộng, băng thông của HBM vượt xa DDR hay GDDR (suy luận của người viết từ cấu trúc bus rộng).

Số liệu các thế hệ: HBM3E 12 lớp của Micron dung lượng 36 GB mỗi stack, băng thông trên 1,2 TB/s, tốc độ trên 9,2 Gb/s mỗi chân [S30]. Chuẩn JEDEC HBM4 hỗ trợ giao diện 2048 bit, tốc độ đến 8 Gb/s mỗi chân, băng thông đến 2 TB/s, xếp từ 4 đến 16 lớp, dung lượng đến 64 GB mỗi stack, và 32 kênh thay vì 16 kênh của HBM3 [S29]. Samsung và Micron đã bắt đầu giao HBM4 từ tháng 2 năm 2026, đúng lúc Nvidia chuẩn bị nền tảng Vera Rubin [S31]. Bài không có nguồn đọc được cho thông số HBM2e.

**CXL** (Compute Express Link) là chuẩn kết nối chạy trên tầng vật lý của PCIe, có thêm các giao thức nhất quán bộ nhớ đệm (cache-coherent) để CPU truy cập bộ nhớ của thiết bị [S32]. Một thẻ nhớ CXL cho phép **mở rộng dung lượng RAM** mà không cần thêm khe DIMM; Samsung đã công bố từ năm 2021 một module mở rộng 128 GB dựa trên DDR5 [S32]. Vị trí của nó nằm giữa RAM gắn trực tiếp và SSD: chậm hơn RAM tại chỗ nhưng nhanh hơn SSD rất nhiều (suy luận của người viết; các nguồn đo độ trễ CXL còn lệch nhau nên bài không nêu con số).

## So sánh và hướng dẫn chọn

Bảng dưới là bản tổng hợp từ các mục trên, mọi số là số tham khảo tính đến 11/2026.

| Loại | Bay hơi? | Tốc độ/độ trễ (bậc độ lớn) | Dung lượng hiện hành | Giá tham khảo | Ứng dụng |
|---|---|---|---|---|---|
| Cache SRAM | Có | khoảng 1 đến 10 ns | KB đến chục MB | rất đắt | trong CPU |
| RAM DDR5 | Có | khoảng 50 đến 100 ns | GB đến trăm GB | khoảng 13 đến 19 USD/GB [S34] | RAM chính |
| HBM | Có | băng thông trên 1,2 TB/s mỗi stack [S30] | 36 GB đến 64 GB mỗi stack [S29][S30] | không có nguồn giá | GPU và AI |
| SSD NVMe | Không | đọc tuần tự đến 13,7 GB/s (PCIe 5.0) [S13] | đến 245 TB [S13] | khoảng 0,08 đến 0,19 USD/GB [S36] | ổ chính, server |
| SSD SATA | Không | tối đa 600 MB/s [S9] | TB | tương tự SSD | nâng cấp máy cũ |
| HDD | Không | khoảng 5 đến 15 ms | đến 36 TB đã bán, 40 TB đang giao hạn chế [S3][S4] | khoảng 0,02 đến 0,04 USD/GB [S35] | NAS, backup |
| Băng LTO | Không | chậm, tuần tự | 40 TB gốc [S19] | không có nguồn giá | lưu trữ dài hạn |

Hướng dẫn chọn theo nhu cầu (suy luận của người viết từ các đặc tính trên):
- **PC văn phòng:** một SSD SATA hoặc NVMe 500 GB đến 1 TB và 16 GB RAM là đủ; không cần ổ nhanh nhất.
- **Laptop:** SSD NVMe M.2 cho lưu trữ; RAM LPDDR gắn sẵn hoặc DDR5 SO-DIMM; ưu tiên tiết kiệm pin.
- **Gaming:** SSD NVMe PCIe 4.0 hoặc 5.0 cho tải game; RAM DDR5; GPU có GDDR riêng.
- **Workstation:** RAM lớn có thể có ECC, SSD NVMe nhanh cho dự án đang làm, HDD cho kho dữ liệu cũ.
- **NAS:** ổ HDD CMR dung lượng lớn; thêm một SSD làm bộ đệm nếu cần.
- **Server:** SSD NVMe doanh nghiệp U.2 hoặc EDSFF, RAM RDIMM có ECC, có thể thêm CXL.
- **AI/GPU:** GPU dùng HBM; dữ liệu huấn luyện đặt trên SSD NVMe nhanh.
- **Backup/archive:** HDD dung lượng lớn cho bản sao gần; băng từ LTO cho lưu dài hạn.

## Hiểu lầm thường gặp

- **"RAM là một loại ổ đĩa."** Sai: RAM và HBM là bộ nhớ bay hơi, mất dữ liệu khi tắt điện; ổ đĩa lưu trữ mới giữ dữ liệu [S4][S23].
- **"SSD mau hỏng hơn HDD, nên không dùng được."** SSD có giới hạn số lần ghi và độ bền được công bố bằng TBW hoặc DWPD [S4]; với mức ghi thông thường của người dùng, giới hạn đó thường lớn (suy luận từ ví dụ 600 TBW: khoảng 330 GB ghi mỗi ngày trong 5 năm).
- **"NVMe luôn nhanh gấp nhiều lần SATA khi dùng thật."** Tốc độ tuần tự khác xa [S9][S13], nhưng việc mở ứng dụng hay duyệt web phụ thuộc cả độ trễ và phần mềm; sự khác biệt cảm nhận được nhỏ hơn nhiều (suy luận của người viết).
- **"Ổ NAS nào cũng như nhau."** Ổ SMR có thể ghi ngẫu nhiên chậm vì phải ghi lại cả chuỗi track [S2]; nên xem ổ là CMR hay SMR trước khi mua.
- **"HBM là RAM tốt hơn, cứ thay vào là xong."** HBM nằm cạnh GPU trên interposer và được đóng gói cùng bộ xử lý, nên không cắm vào khe DIMM như DDR [S28].
- **"Optane vẫn mua được và là tương lai."** Intel đã ngừng kinh doanh Optane [S21].

## Điều cần nhớ và độ chắc chắn của số liệu

Năm điều cần nhớ: RAM và HBM là bộ nhớ bay hơi, còn HDD, SSD và băng từ là lưu trữ không bay hơi. Kim tự tháp bộ nhớ đổi tốc độ lấy dung lượng và giá. HDD rẻ và lớn nhưng chậm vì phải dò và chờ đĩa quay. SSD nhanh vì không có bộ phận chuyển động; loại cell (SLC đến QLC) và giao diện (SATA hay NVMe) quyết định giá, độ bền và tốc độ. HBM nhanh nhờ xếp chồng die, nối TSV và đặt sát GPU.

Điểm chưa chắc chắn: (1) độ trễ của cache, DRAM, SSD, HDD trong bài là bậc độ lớn thuộc kiến thức nền, không kèm nguồn; (2) giá lấy từ hai trang theo dõi giá bán lẻ (thứ cấp), biến động mạnh, và giá SSD là phép tự tính từ một mẫu 130 ổ; (3) độ bền QLC, số tầng 3D NAND của Samsung và Micron, tốc độ tối đa JEDEC của DDR5, thông số GDDR7 và HBM2e, và độ trễ CXL chính xác đều chưa có nguồn đọc được nên bài không nêu số; (4) Seagate 40 TB mới giao giới hạn theo nguồn đã đọc, còn tình trạng sẵn có cuối 2026 chưa kiểm; (5) bài không đánh giá thương hiệu hay model cụ thể.

## Nguồn tham khảo

- [S1] [Wikipedia, Hard disk drive](https://en.wikipedia.org/wiki/Hard_disk_drive)
- [S2] [Wikipedia, Shingled magnetic recording](https://en.wikipedia.org/wiki/Shingled_magnetic_recording)
- [S3] [TechRadar, Seagate confirms 40TB hard drives have already been shipped (2025)](https://www.techradar.com/pro/seagate-confirms-40tb-hard-drives-have-already-been-shipped-but-dont-expect-them-to-go-on-sale-till-2026)
- [S4] [Wikipedia, Solid-state drive](https://en.wikipedia.org/wiki/Solid-state_drive)
- [S5] [Wikipedia, Multi-level cell](https://en.wikipedia.org/wiki/Multi-level_cell)
- [S6] [Wikipedia, V-NAND (3D NAND)](https://en.wikipedia.org/wiki/V-NAND)
- [S7] [Enterprise Storage Forum, Understanding Multilayer SSDs: SLC, MLC, TLC, QLC, and PLC (2023)](https://www.enterprisestorageforum.com/hardware/understanding-multilayer-ssds)
- [S8] [Wikipedia, NVM Express](https://en.wikipedia.org/wiki/NVM_Express)
- [S9] [Wikipedia, Serial ATA](https://en.wikipedia.org/wiki/Serial_ATA)
- [S10] [SNIA, SSD Form Factors (cập nhật 10/2026)](https://www.snia.org/forums/cmsi/knowledge/formfactors)
- [S11] [Tom's Hardware, PCIe 7.0 spec finalized (2025)](https://www.tomshardware.com/tech-industry/pcie-7-0-spec-finalized-with-up-to-512gb-s-speeds-pci-sig-targets-1tb-s-for-8-0-as-exploration-phase-begins)
- [S12] [StorageReview, Micron 9650 NVMe SSD Enters Mass Production (2026)](https://www.storagereview.com/news/micron-9650-nvme-ssd-enters-mass-production-as-first-pcie-gen6-enterprise-ssd)
- [S13] [StorageReview, Micron 6600 ION 245TB SSD Review (2026)](https://www.storagereview.com/review/micron-6600-ion-245tb-ssd-review-a-quarter-petabyte-per-drive-bay)
- [S14] [TrendForce, SK hynix Reportedly Eyes 321-Layer QLC NAND in 2H26 (2025)](https://www.trendforce.com/news/2025/11/11/news-sk-hynix-reportedly-eyes-321-layer-qlc-nand-in-2h26-future-of-solidigm-ipo-uncertain/)
- [S15] [Wikipedia, Flash memory](https://en.wikipedia.org/wiki/Flash_memory)
- [S16] [JEDEC, Updates to UFS and memory interface standards (UFS 5.0, 2026)](https://www.jedec.org/node/9631)
- [S17] [Wikipedia, Compact disc](https://en.wikipedia.org/wiki/Compact_disc)
- [S18] [Wikipedia, Linear Tape-Open](https://en.wikipedia.org/wiki/Linear_Tape-Open)
- [S19] [Tom's Hardware, Fujifilm to begin shipping 40TB LTO Ultrium 10 cartridges (2025)](https://www.tomshardware.com/pc-components/storage/fujifilm-to-begin-shipping-lto-ultrium-10-40tb-tape-cartridges-in-january-2026)
- [S20] [Wikipedia, 3D XPoint (Optane)](https://en.wikipedia.org/wiki/3D_XPoint)
- [S21] [Tom's Hardware, Intel Kills Optane Memory Business, Pays $559 Million to Exit (2022)](https://www.tomshardware.com/news/intel-kills-optane-memory-business-for-good)
- [S22] [Wikipedia, Static random-access memory](https://en.wikipedia.org/wiki/Static_random-access_memory)
- [S23] [Wikipedia, Dynamic random-access memory](https://en.wikipedia.org/wiki/Dynamic_random-access_memory)
- [S24] [Wikipedia, DDR5 SDRAM](https://en.wikipedia.org/wiki/DDR5_SDRAM)
- [S25] [Wikipedia, DIMM](https://en.wikipedia.org/wiki/DIMM)
- [S26] [Wikipedia, ECC memory](https://en.wikipedia.org/wiki/ECC_memory)
- [S27] [Wikipedia, GDDR SDRAM](https://en.wikipedia.org/wiki/GDDR_SDRAM)
- [S28] [Wikipedia, High Bandwidth Memory](https://en.wikipedia.org/wiki/High_Bandwidth_Memory)
- [S29] [Tom's Hardware, JEDEC finalizes HBM4 memory standard (2025)](https://www.tomshardware.com/pc-components/ram/jedec-finalizes-hbm4-memory-standard-with-major-bandwidth-and-efficiency-upgrades)
- [S30] [Tom's Hardware, Micron ships production-ready 12-Hi HBM3E chips (2024)](https://www.tomshardware.com/pc-components/gpus/micron-ships-production-ready-12-hi-hbm3e-chips-for-next-gen-ai-gpus-up-to-36gb-per-stack-with-speeds-surpassing-92-gts)
- [S31] [The Register, Samsung and Micron start shipping HBM4 (2026)](https://www.theregister.com/2026/02/13/samsung_and_micron_start_shipping/)
- [S32] [Wikipedia, Compute Express Link](https://en.wikipedia.org/wiki/Compute_Express_Link)
- [S33] [Wikipedia, USB flash drive](https://en.wikipedia.org/wiki/USB_flash_drive)
- [S34] [Capital and Compute, RAM prices in 2026 (tracker cập nhật 3/11/2026)](https://capitalandcompute.net/memory-prices/)
- [S35] [Storage Disk Prices, Hard drive prices live by $/TB (2026)](https://storagediskprices.com/hdd-prices/)
- [S36] [Storage Disk Prices, SSD prices live by $/TB (2026)](https://storagediskprices.com/ssd-prices/)
