---
id: L19
title: Transistor cho người mới: hình dạng, ký hiệu và dòng điện
topic: ky-thuat
date: 2026-10-28
---
# Transistor cho người mới: hình dạng, ký hiệu và dòng điện

Câu hỏi mở bài: một linh kiện ba chân nhỏ bằng hạt đậu làm sao vừa khuếch đại tín hiệu, vừa đóng ngắt được dòng điện lớn, và mỗi loại (NPN, PNP, MOSFET kênh N, kênh P, JFET) khác nhau ở đâu?

Bài dành cho kỹ sư không chuyên điện tử. Mọi hình, ký hiệu và sơ đồ dòng điện trong deck dùng **một màu cố định cho mỗi cực**: cực điều khiển Base/Gate màu cam, cực Collector/Drain màu xanh dương, cực Emitter/Source màu xanh lục. Dòng điều khiển vẽ mũi tên cam mảnh, dòng chính vẽ mũi tên xanh dương đậm. Mọi chiều dòng điện trong bài là **chiều quy ước** (conventional current, từ cực dương sang cực âm).

## Transistor là gì và để làm gì

Transistor là linh kiện bán dẫn (semiconductor) ba cực: một tín hiệu nhỏ đặt vào một cực điều khiển dòng điện lớn chạy giữa hai cực còn lại [S1]. Nhờ vậy nó làm được hai việc: **khuếch đại** (amplify) tín hiệu và **đóng/ngắt** (switch) như một công tắc điện tử [S1][S3].

Hình dung một van nước: bạn xoay tay van bằng một lực nhỏ, và dòng nước lớn trong ống chảy nhiều hay ít theo. Tài liệu về JFET cũng dùng đúng hình ảnh này: dòng nước qua ống vòi được điều khiển bằng cách bóp ống, và dòng điện qua JFET được điều khiển bằng cách thắt kênh dẫn [S4]. Tay van là cực điều khiển, ống nước là hai cực còn lại.

Tên ba cực phụ thuộc họ linh kiện [S2][S3][S4]:

- Cực điều khiển: **cực gốc** (Base) ở BJT, **cổng** (Gate) ở FET.
- Cực dòng chính vào: **cực thu** (Collector) ở BJT, **máng** (Drain) ở FET.
- Cực dòng chính ra: **cực phát** (Emitter) ở BJT, **nguồn** (Source) ở FET.

Hai cách điều khiển cần nhớ: BJT thường được hiểu là điều khiển bằng **dòng** Base, còn FET điều khiển bằng **điện áp** giữa Gate và Source [S1][S3][S4]. Mô hình "dòng Base điều khiển dòng Collector" là mô hình dễ dùng nhất khi mới học; tài liệu BJT cũng nói dòng Collector–Emitter có thể xem là do dòng Base–Emitter hoặc do điện áp Base–Emitter điều khiển, hai cách nhìn này liên hệ với nhau qua đường cong dòng–áp của mối nối Base–Emitter [S2].

## Bản đồ phân loại

Transistor chia thành hai họ lớn: **BJT** (bipolar junction transistor, transistor lưỡng cực) và **FET** (field-effect transistor, transistor hiệu ứng trường) [S1].

- **BJT** có hai loại theo thứ tự lớp bán dẫn: **NPN** và **PNP** [S2][S5].
- **FET** gồm **MOSFET** (cổng cách điện bằng lớp oxit) và **JFET** (cổng là một mối nối p–n) [S3][S4].
- Mỗi loại FET có **kênh N** (N-channel, dòng chủ yếu do electron) hoặc **kênh P** (P-channel, dòng chủ yếu do lỗ trống) [S3][S4].

MOSFET còn chia thành loại tăng cường (enhancement, mặc định tắt, cần điện áp Gate để bật) và loại suy giảm (depletion) [S3]. Bài này chỉ vẽ loại tăng cường, loại thường gặp nhất khi dùng làm công tắc. JFET thì ngược lại: thường dẫn khi điện áp Gate–Source bằng không [S4].

Bốn loại chính của bài: **NPN, PNP, MOSFET kênh N, MOSFET kênh P**. JFET được nói ngắn gọn.

## Hình dạng thực tế và cách nhận biết chân

Cùng một chức năng có thể nằm trong nhiều kiểu vỏ (package). Danh sách vỏ xuyên lỗ (through-hole) phổ biến gồm TO-92, TO-126, TO-220 và nhiều kiểu khác; vỏ dán bề mặt (surface-mount, SMD) thì nhiều hơn hẳn [S1].

- **TO-92**: vỏ nhựa nhỏ, một mặt phẳng, ba chân thẳng hàng; dùng cho transistor tín hiệu nhỏ [S1]. Ảnh BC547 và 2N3906 trong deck là loại này [S11][S12].
- **SOT-23**: vỏ dán rất nhỏ, ba chân (hai chân một bên, một chân bên kia) [S8][S12]. Trong ảnh so sánh kích thước, SOT-23 nhỏ hơn TO-92 nhiều lần [S12].
- **TO-220**: vỏ công suất xuyên lỗ, có tấm kim loại bắt tản nhiệt (heatsink) [S9]. Trên MOSFET và BJT công suất, tấm này thường nối điện với Drain hoặc Collector, nên đọc datasheet trước khi bắt chung lên tản nhiệt. Ảnh MOSFET FQP30N06L cắm trên bảng thử mạch trong deck là loại này [S18]. Bản "fullpak" trong ảnh IRFI9540 và IRFIBC30 có thân nhựa bọc kín, cách điện với tản nhiệt [S14][S15].
- **D2PAK**: vỏ công suất dán bề mặt. Ảnh của bài có que diêm làm thước đo; mỗi linh kiện trong ảnh chịu được điện áp chặn 120 V và dòng liên tục 30 A khi có tản nhiệt phù hợp [S10][S13].

**Thứ tự chân không chung cho mọi linh kiện cùng vỏ.** Trên thân chiếc 2N3906 trong ảnh có in sẵn "EBC" [S12]; linh kiện khác trong cùng vỏ TO-92 có thể xếp chân khác. Với MOSFET IRLZ24N trong vỏ TO-220 nhìn từ mặt có chữ, ba chân từ trái sang phải là Gate, Drain, Source [S10]. Quy tắc an toàn: luôn đối chiếu mã ghi trên thân với datasheet của đúng linh kiện đó.

## BJT NPN

**Nhận dạng.** NPN có ba chân Base, Collector, Emitter. Trên ký hiệu, mũi tên nằm ở Emitter và **chỉ ra ngoài**; mẹo nhớ "Not Pointing iN" (không chỉ vào trong) [S5]. Mũi tên trùng với chiều của diode Base–Emitter, cho biết chiều dòng điện đi qua transistor [S5]. Ảnh thật trong deck là BC547 vỏ TO-92 [S11].

**Cách điều khiển.** NPN được bật bằng **dòng** chảy vào Base. Điều kiện để Base–Emitter bắt đầu dẫn là V_BE vượt ngưỡng khoảng 0,6 V (nhiều giáo trình làm tròn thành 0,7 V; giá trị thật thay đổi theo linh kiện và nhiệt độ) [S5]. Dưới ngưỡng này transistor ở chế độ ngắt (cutoff), không có dòng C–E; khi Base đủ cao nó đóng vai một đường nối gần như ngắn mạch từ Collector sang Emitter (chế độ bão hòa, saturation) [S5].

**Dòng điện.** Dòng Base I_B nhỏ chảy vào Base, dòng chính I_C chảy từ Collector sang Emitter, và hai dòng này cùng ra khỏi Emitter: I_E = I_C + I_B. Trong vùng khuếch đại (active mode), I_C ≈ β × I_B, với β là độ lợi dòng (current gain) của linh kiện [S2]. Ví dụ minh họa (số giả định): β = 100 và I_B = 1 mA cho I_C = 100 mA và I_E = 101 mA. β không phải hằng số vật lý cố định mà thay đổi theo linh kiện và điều kiện làm việc [S2]. Khi dùng làm công tắc, người thiết kế thường cấp dòng Base dư để transistor bão hòa thay vì tính theo β.

**Mạch ví dụ: bật/tắt LED hoặc relay (low-side switch).** Tải (LED có điện trở hạn dòng, hoặc cuộn relay) nối giữa nguồn dương và Collector; Emitter nối đất; tín hiệu từ vi điều khiển đi qua một **điện trở Base** vào Base. Khi chân điều khiển ở mức cao, dòng Base chảy, transistor dẫn và tải sáng/đóng; khi ở mức thấp, tải tắt. Vì transistor nằm ở phía thấp (nối đất) của mạch nên gọi là low-side switch [S5]. Điện trở Base là bắt buộc để giới hạn dòng Base [S5]. Với cuộn relay (tải cảm), nên mắc thêm diode bảo vệ song song cuộn dây để dập xung điện áp khi ngắt (thực hành thiết kế thông dụng).

## BJT PNP

**Khác biệt cốt lõi so với NPN:** mọi chiều đảo ngược. Trên ký hiệu, mũi tên ở Emitter **chỉ vào trong** [S5]. Dòng chính chảy từ **Emitter sang Collector**, và dòng Base chảy **ra khỏi** Base [S5]. Mô tả vận hành của PNP chỉ cần đảo cực tính so với NPN [S5].

**Cách bật.** Emitter nối vào điện áp cao (nguồn dương); để bật, phải kéo Base xuống thấp hơn Emitter khoảng 0,6 V (V_EB ≈ 0,6–0,7 V) [S5]. Muốn tắt, Base phải được đưa về xấp xỉ điện áp Emitter [S5]. Ảnh thật trong deck là 2N3906, một PNP vỏ TO-92 [S12].

**Mạch ví dụ: high-side switch.** Emitter nối nguồn dương, tải nối giữa Collector và đất; PNP nằm ở phía cao của mạch [S5]. Một cạm bẫy được nêu rõ trong tài liệu: nếu nguồn của tải cao hơn điện áp mức cao của tín hiệu điều khiển (ví dụ vi điều khiển 5 V điều khiển tải 12 V), Base không bao giờ lên đủ cao để tắt PNP, nên mạch không tắt được [S5].

## MOSFET kênh N

**Nhận dạng.** MOSFET có ba chân Gate, Drain, Source. Cổng được cách điện bằng lớp oxit nên điện áp Gate quyết định độ dẫn điện của linh kiện [S3]. Ký hiệu có Gate tách rời khỏi kênh, mũi tên trên đường Source của kênh N **chỉ vào** phía kênh. Ảnh thật trong deck là IRFIBC30, MOSFET công suất vỏ TO-220 fullpak [S15].

**Cách điều khiển.** Điều khiển bằng **điện áp**: khi V_GS vượt ngưỡng V_th (threshold voltage), một lớp đảo (inversion layer) hình thành và kênh dẫn nối Drain với Source [S3]. Vì cổng được cách điện, ở trạng thái tĩnh (DC) gần như không có dòng Gate. Cổng vẫn có điện dung, nên khi đóng ngắt nhanh vẫn cần một dòng nạp/xả ngắn cho cổng. V_th là ngưỡng bắt đầu dẫn; để bật hẳn, datasheet quy định điện trở R_DS(on) ở một mức V_GS cụ thể, nên đừng chọn linh kiện chỉ theo V_th. Với vi điều khiển 5 V hoặc 3,3 V, hãy tìm loại có R_DS(on) được ghi ở V_GS thấp (logic-level).

**Dòng điện.** Dòng I_D chảy từ **Drain sang Source**. Ở trạng thái bật, giữa Drain và Source linh kiện xử sự như một điện trở R_DS(on) [S10].

**Mạch ví dụ: low-side switch.** Source nối đất; tải nối giữa nguồn dương và Drain; tín hiệu điều khiển vào Gate (qua điện trở nhỏ hạn chế dòng nạp cổng; thêm điện trở kéo xuống giữa Gate và Source để giữ tắt khi chân điều khiển để hở). Khi V_GS > V_th (đủ lớn), I_D chảy và tải hoạt động.

## MOSFET kênh P

**Khác biệt cốt lõi:** cực tính đảo ngược. Mũi tên trên đường kênh chỉ **ra ngoài**. MOSFET kênh P **bật khi V_GS âm**, tức Gate thấp hơn Source một khoảng vượt ngưỡng |V_th|; dòng I_D chảy từ **Source sang Drain**. Ảnh thật trong deck là IRFI9540, MOSFET kênh P công suất vỏ TO-220 fullpak [S14].

**High-side switch.** Source nối nguồn dương, Drain nối tải, tải nối đất. Kéo Gate về đất (thấp hơn Source) thì bật; đưa Gate về bằng điện áp Source (V_GS ≈ 0) thì tắt. Cách này tiện vì tải vẫn nối đất, nhưng cần kiểm tra điện áp V_GS tối đa cho phép trong datasheet khi nguồn cao.

**Cấu trúc bán dẫn (electron và hole).** MOSFET kênh N xây trên đế loại P: điện áp Gate dương kéo electron lên bề mặt tạo kênh dẫn loại N giữa hai vùng N của Source và Drain. MOSFET kênh P xây ngược lại, trên đế loại N với hai vùng P: điện áp Gate âm kéo lỗ trống (hole) lên bề mặt tạo kênh loại P [S3]. Nói gọn: kênh N dẫn bằng electron, kênh P dẫn bằng lỗ trống.

## JFET

JFET là một trong những loại FET đơn giản nhất [S4]. Nó là kênh bán dẫn dài với hai tiếp xúc ở hai đầu (Source, Drain) và một mối nối p–n làm Gate [S4]. Khác BJT, JFET hoàn toàn điều khiển bằng điện áp, không cần dòng phân cực [S4].

**Điều khiển.** JFET thường dẫn khi điện áp Gate–Source bằng không. Đặt điện áp ngược (reverse bias) lên Gate thì lớp nghèo (depletion layer) mở rộng, kênh bị bóp lại; đến điện áp pinch-off thì dòng Drain–Source ngừng [S4]. Với kênh N, Gate âm hơn Source làm dòng giảm; với kênh P thì ngược lại [S4]. Trở kháng vào của JFET lớn, có tài liệu nêu cỡ 10^10 Ω [S4].

**Ký hiệu và ảnh.** Ký hiệu JFET kênh N có mũi tên ở Gate chỉ vào kênh. Ảnh thật trong deck là một JFET vỏ TO-92 có chữ K170 trên thân [S16]. Dùng JFET làm công tắc hoặc điện trở điều khiển bằng điện áp, hoặc xây mạch khuếch đại [S4].

## So sánh BJT và MOSFET

- **Điều khiển bằng gì**: BJT bằng dòng Base (mô hình thực hành); MOSFET bằng điện áp Gate [S2][S3].
- **Trở kháng vào**: BJT thấp hơn vì phải cấp dòng Base; MOSFET rất cao ở DC vì cổng cách điện [S3], nhưng cổng có điện dung.
- **Tốc độ chuyển mạch**: MOSFET công suất là linh kiện đơn cực (unipolar) nên đóng ngắt rất nhanh, không phải chờ xả hạt tải thiểu số như transistor lưỡng cực [S10]. Con số cụ thể tùy từng linh kiện.
- **Tổn hao**: BJT bão hòa có sụt áp V_CE(sat) giữa C và E [S5]; MOSFET bật có điện trở R_DS(on), nên tổn hao dẫn tính theo dòng bình phương nhân điện trở [S10]. Với dòng lớn, MOSFET có R_DS(on) nhỏ thường ít nóng hơn.
- **Ứng dụng điển hình**: BJT cho khuếch đại tín hiệu nhỏ và công tắc tải nhỏ [S5]; MOSFET cho công tắc công suất, điều khiển động cơ và logic số CMOS [S6][S10].

## Bảng tổng hợp ký hiệu

Bốn ký hiệu đặt cạnh nhau, mỗi loại ghi chiều mũi tên và chiều dòng điện chính (chiều quy ước):

| Loại | Mũi tên | Dòng chính | Điều kiện bật |
|---|---|---|---|
| NPN | ở Emitter, chỉ ra ngoài [S5] | Collector → Emitter | Base cao hơn Emitter khoảng 0,6 V [S5] |
| PNP | ở Emitter, chỉ vào trong [S5] | Emitter → Collector | Base thấp hơn Emitter khoảng 0,6 V [S5] |
| MOSFET kênh N | trên đường Source, chỉ vào kênh | Drain → Source | V_GS > V_th, dương [S3] |
| MOSFET kênh P | trên đường Source, chỉ ra ngoài kênh | Source → Drain | V_GS < −|V_th|, âm [S3] |

Mẹo nhớ cho BJT: mũi tên NPN "không chỉ vào trong", mũi tên PNP chỉ vào trong [S5]. Với MOSFET ba cực, mũi tên chỉ vào kênh là kênh N, chỉ ra ngoài là kênh P.

## Đo kiểm bằng đồng hồ vạn năng

Dùng thang đo diode của đồng hồ số. Cách đo dựa trên mô hình "hai diode nối lưng nhau": diode Base–Emitter và diode Base–Collector [S5]. Tài liệu nhắc rằng mô hình này chỉ dùng để kiểm tra, không dùng để hiểu hoạt động của transistor [S5].

**BJT NPN** (đồng hồ số: que đỏ là cực +, que đen là cực −):

1. Que đỏ vào Base, que đen lần lượt vào Collector rồi Emitter: đồng hồ hiện sụt áp thuận, cỡ vài trăm milivôn đến khoảng 0,7 V.
2. Đảo que (đen vào Base, đỏ lần lượt vào C và E): đồng hồ báo hở (OL).
3. Giữa Collector và Emitter, cả hai chiều: OL.

**BJT PNP**: kết quả đảo lại, que **đen** vào Base thì hai mối nối dẫn.

**MOSFET**: Gate cách điện nên Gate với Drain và Gate với Source đều báo OL ở cả hai chiều. Giữa Drain và Source, linh kiện công suất có diode thân (body diode) cho kết quả như một diode: kênh N dẫn khi que đỏ ở Source, que đen ở Drain; kênh P dẫn theo chiều ngược lại. Cổng MOSFET nhạy với tĩnh điện (ESD): chạm que nối đất vào cả ba chân hoặc nối tắt Gate–Source để xả điện tích trước khi đo.

Giới hạn: đo ngay trên bo mạch cho kết quả sai vì các linh kiện khác mắc song song; tháo chân hoặc tháo linh kiện ra khi cần chắc chắn. Mức sụt áp chính xác phụ thuộc đồng hồ và linh kiện.

## Ứng dụng thực tế

- **Công tắc**: bật/tắt LED, relay, van bằng tín hiệu nhỏ từ vi điều khiển, như các mạch low-side và high-side ở trên [S5].
- **Khuếch đại**: mạch bám Emitter (emitter follower) dùng như bộ khuếch đại dòng và bộ đệm điện áp; cặp Darlington nhân độ lợi dòng của hai transistor [S5].
- **Vi mạch số CMOS**: CMOS dùng các **cặp đối xứng MOSFET loại P và loại N** để làm cổng logic; cổng đảo (NOT) gồm một PMOS và một NMOS [S6]. Vi xử lý, vi điều khiển và bộ nhớ đều làm bằng CMOS [S6].
- **Điều khiển động cơ**: cầu H (H-bridge) gồm bốn transistor cho phép động cơ quay cả hai chiều [S5].
- **Ô tô**: bộ điều khiển điện tử ECU có các mạch **điều khiển cơ cấu chấp hành** (actuator driver) cho kim phun, relay và van, cùng mạch cầu H cho động cơ servo [S7]. Ảnh bo mạch "main controller" mã 8200607915 của Renault trong deck ghi rõ một transistor NPN BCP56-16 vỏ SOT-223 trên bo [S17]. Tải của kim phun hay bơm thường được đóng/ngắt ở phía thấp bằng kiểu mạch NPN hoặc N-MOSFET như phần trên; thiết kế cụ thể của từng hãng nằm ngoài nguồn của bài.

## Cheat sheet và câu hỏi tự kiểm tra

**Cheat sheet một trang.**

- Ba cực: điều khiển (Base/Gate, cam), dòng chính vào (Collector/Drain, xanh dương), dòng chính ra (Emitter/Source, xanh lục).
- NPN: mũi tên ra ngoài; dòng Base vào; V_BE ≈ 0,6–0,7 V; I_C ≈ β·I_B; I_E = I_C + I_B; dòng C → E; công tắc low-side.
- PNP: mũi tên vào trong; dòng Base ra; Base thấp hơn Emitter ~0,6 V; dòng E → C; công tắc high-side.
- MOSFET kênh N: điều khiển bằng điện áp; bật khi V_GS > V_th; gần như không có dòng Gate (DC); dòng D → S; low-side.
- MOSFET kênh P: bật khi V_GS âm; dòng S → D; high-side.
- JFET: điều khiển bằng điện áp; thường dẫn khi V_GS = 0; V_GS ngược chiều làm kênh bị bóp (pinch-off).

**Năm câu hỏi tự kiểm tra** (đáp án ở cuối mục):

1. Điều kiện giữa Base và Emitter để một NPN silicon bắt đầu dẫn là gì?
2. Một NPN có β = 200 nhận I_B = 0,5 mA. I_C và I_E bằng bao nhiêu (trong vùng khuếch đại)?
3. Dùng N-MOSFET làm công tắc low-side thì tải nối ở đâu và Gate cần điều kiện gì?
4. Muốn bật P-MOSFET làm công tắc high-side, Gate phải ở mức nào so với Source?
5. Vì sao khi V_GS = 0, JFET dẫn còn MOSFET tăng cường thì không?

*Đáp án.* (1) V_BE khoảng 0,6–0,7 V và có dòng chảy vào Base [S5]. (2) I_C ≈ 200 × 0,5 mA = 100 mA; I_E = I_C + I_B = 100,5 mA [S2]. (3) Tải giữa nguồn dương và Drain, Source nối đất, cần V_GS > V_th [S3]. (4) Gate thấp hơn Source quá |V_th| (V_GS âm). (5) JFET có kênh dẫn sẵn và chỉ bị bóp khi Gate phân cực ngược [S4]; MOSFET tăng cường cần điện áp Gate vượt V_th mới tạo kênh [S3].

## Nguồn tham khảo

- [S1] Wikipedia, Transistor, https://en.wikipedia.org/wiki/Transistor
- [S2] Wikipedia, Bipolar junction transistor, https://en.wikipedia.org/wiki/Bipolar_junction_transistor
- [S3] Wikipedia, MOSFET, https://en.wikipedia.org/wiki/MOSFET
- [S4] Wikipedia, JFET, https://en.wikipedia.org/wiki/JFET
- [S5] SparkFun Electronics, Transistors (tutorial), https://learn.sparkfun.com/tutorials/transistors
- [S6] Wikipedia, CMOS, https://en.wikipedia.org/wiki/CMOS
- [S7] Wikipedia, Electronic control unit, https://en.wikipedia.org/wiki/Electronic_control_unit
- [S8] Wikipedia, Small-outline transistor, https://en.wikipedia.org/wiki/Small-outline_transistor
- [S9] Wikipedia, TO-220, https://en.wikipedia.org/wiki/TO-220
- [S10] Wikipedia, Power MOSFET, https://en.wikipedia.org/wiki/Power_MOSFET
- [S11] Suyash Dwivedi, BC547 Transistor - 01.jpg, 2025, CC BY-SA 4.0, Wikimedia Commons, https://commons.wikimedia.org/wiki/File:BC547_Transistor_-_01.jpg
- [S12] Mister rf, Transistorer (cropped).jpg, 2021, CC BY-SA 3.0, Wikimedia Commons, https://commons.wikimedia.org/wiki/File:Transistorer_(cropped).jpg
- [S13] CyrilB, D2PAK.JPG, 2006, CC BY-SA 3.0 hoặc GFDL, Wikimedia Commons, https://commons.wikimedia.org/wiki/File:D2PAK.JPG
- [S14] Retired electrician, IRFI9540 MOS transistor 02.jpg, 2023, CC0, Wikimedia Commons, https://commons.wikimedia.org/wiki/File:IRFI9540_MOS_transistor_02.jpg
- [S15] Retired electrician, IRFIBC30 MOS transistor 01.jpg, 2023, CC0, Wikimedia Commons, https://commons.wikimedia.org/wiki/File:IRFIBC30_MOS_transistor_01.jpg
- [S16] Euler666, Encapsulado JFET.jpg, 2008, CC BY-SA 3.0, Wikimedia Commons, https://commons.wikimedia.org/wiki/File:Encapsulado_JFET.jpg
- [S17] Raimond Spekking, Renault 8200607915 - main controller - On Semiconductor BH-16-7382.jpg, 2018, CC BY-SA 4.0, Wikimedia Commons, https://commons.wikimedia.org/wiki/File:Renault_8200607915_-_main_controller_-_On_Semiconductor_BH-16-7382.jpg
- [S18] Axel Richter, Mosfet (ảnh MOSFET FQP30N06L vỏ TO-220), Unsplash License, https://unsplash.com/photos/w03bBxjXWvk
