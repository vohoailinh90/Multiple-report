---
id: L22
title: OKX trong giao dịch: sàn, sản phẩm, tài khoản, phí và rủi ro
topic: khac
date: 2026-11-12
---
# OKX trong giao dịch: sàn, sản phẩm, tài khoản, phí và rủi ro

Câu hỏi của bài: OKX là sàn như thế nào, bạn giao dịch được gì ở đó, tài khoản ký quỹ và hợp đồng vĩnh cửu vận hành ra sao, phí và funding lấy đi bao nhiêu, và còn những rủi ro nào mà một trang chủ đẹp không nói thay bạn?

Bài đọc từ tài liệu **của chính OKX** (trang Learn, trang trợ giúp, tài liệu API, trang phí, trang Proof of Reserves) cộng một nguồn bên ngoài là Wikipedia. Câu có `[Sn]` là điều nguồn nói; câu ghi "Tự tính" hay "Suy luận của người viết" là phần người viết thêm. Đây là bài học về cách một sàn vận hành, **không phải lời khuyên đầu tư**.

## Tóm tắt

OKX là một sàn giao dịch tiền mã hóa (cryptocurrency exchange) tập trung, tiền thân là Okcoin lập năm 2013 và đổi tên từ OKEx thành OKX năm 2022 [S1]. Trên một nền tảng, người dùng có giao ngay (spot), giao dịch ký quỹ (margin), hợp đồng vĩnh cửu (perpetual swap), hợp đồng kỳ hạn (futures) và quyền chọn (options) [S8]. Điểm cốt lõi là **tài khoản hợp nhất** (unified account): một tài khoản dùng cho cả giao ngay lẫn phái sinh, với bốn chế độ từ đơn giản đến ký quỹ danh mục [S2].

Ba điều quyết định chi phí và rủi ro thực tế của bạn: đòn bẩy và ký quỹ (margin), funding của hợp đồng vĩnh cửu [S3][S5], và bậc phí theo khu vực [S7]. OKX công bố Proof of Reserves để người dùng tự kiểm tra tài sản dự trữ, nhưng đó là báo cáo do chính OKX phát hành [S6].

## OKX là gì và lịch sử

**OKX** là một sàn tiền mã hóa quốc tế đa ngôn ngữ; Wikipedia ghi OKX khởi đầu là Okcoin do Star Xu lập năm 2013 (câu này trong Wikipedia còn mang nhãn "cần dẫn nguồn"), ra mắt dưới tên OKEx năm 2017 ở Hồng Kông, và đổi tên thành OKX năm 2022 [S1].

Lịch sử có cả mốc thuận lợi lẫn mốc rủi ro. Tháng 7/2018, một nhà giao dịch bị cho là đã mua hợp đồng bitcoin tương lai trị giá danh nghĩa 416 triệu USD bằng ký quỹ rồi bị sàn buộc thanh lý lỗ nặng; quỹ bảo hiểm của sàn bơm 2.500 BTC, nhưng để bù phần còn thiếu, những người đang có lãi chưa thực hiện trong tuần trước vẫn bị thu hồi lãi theo tỷ lệ 17%, gọi là "socialized clawback" [S1]. Tháng 10/2020 OKX tạm ngừng rút tiền khi người sáng lập hợp tác với một cuộc điều tra của cảnh sát, rồi mở lại vào cuối tháng 11/2020 [S1]. Tháng 10/2021 sàn thông báo ngừng phục vụ khách hàng ở Trung Quốc đại lục do quy định mới [S1].

Về pháp lý, Wikipedia ghi: giấy phép tài sản ảo tạm thời ở Dubai (7/2022), đơn xin giấy phép ở Hồng Kông (3/2023), thành lập pháp nhân ở Pháp (4/2023), và tháng 4/2025 OKX hoạt động trở lại tại Mỹ với trụ sở ở San Jose, California [S1]. Về vốn, Wikipedia ghi tháng 3/2026 Intercontinental Exchange (công ty mẹ của NYSE) đầu tư và định giá OKX ở mức 25 tỷ USD [S1]. **Đừng hiểu nhầm**: những dòng này là tổng hợp của Wikipedia, một nguồn ai cũng sửa được; bài không đọc trực tiếp từng nguồn gốc mà Wikipedia dẫn.

Token riêng của sàn là **OKB**; năm 2025 OKX công bố đổi mô hình kinh tế của token này để OKB thành token gas duy nhất của mạng X Layer [S1].

## Sản phẩm giao dịch trên OKX

Tài liệu API của OKX phân loại công cụ giao dịch thành năm loại (`instType`): SPOT (giao ngay), MARGIN (ký quỹ), SWAP (hợp đồng vĩnh cửu), FUTURES (hợp đồng kỳ hạn) và OPTION (quyền chọn) [S8]. Đây là cách nhìn gọn nhất về những gì có thể giao dịch.

Menu của chính OKX (bản Hoa Kỳ) mô tả thêm các nhóm sản phẩm xung quanh: Spot để mua bán tiền mã hóa; Futures để giao dịch hợp đồng vĩnh cửu và hợp đồng kỳ hạn có đòn bẩy; TradFi để giao dịch cổ phiếu, ETF và hàng hóa bằng tiền mã hóa; Events & Options; bot giao dịch (trading bots) và sao chép giao dịch (copy trading); Earn và Loan; cùng bộ công cụ cho đại lý AI (Agent Trade Kit) [S7]. **Đừng hiểu nhầm**: đây là menu của bản Hoa Kỳ; sản phẩm có sẵn khác nhau theo khu vực, và chính OKX ghi rằng một số bài viết "có thể không áp dụng cho mọi khách hàng" [S5].

Loại lệnh cũng được liệt kê trong tài liệu API: `market` (khớp ngay theo giá thị trường, chỉ cho SPOT, MARGIN, FUTURES, SWAP), `limit` (lệnh giới hạn), `post_only` (chỉ đặt sổ lệnh, không khớp ngay), `fok` (khớp toàn bộ hoặc hủy) và `ioc` (khớp phần có thể, hủy phần còn lại) [S8].

## Tài khoản hợp nhất và các chế độ ký quỹ

**Tài khoản hợp nhất** (unified account) là tài khoản gộp do OKX thiết kế để dùng chiến lược đồng thời trên giao ngay và các phái sinh như hợp đồng vĩnh cửu, kỳ hạn và quyền chọn, không cần chuyển vốn qua lại giữa nhiều tài khoản [S2]. OKX nêu ba lợi ích: trải nghiệm gọn hơn, hiệu quả vốn tốt hơn vì lãi lỗ ở các thị trường khác nhau có thể bù trừ, và quản trị rủi ro dựa trên tổng vị thế và tổng nợ trong tài khoản [S2].

Có **bốn chế độ tài khoản** [S2]:

- **Chế độ đơn giản** (simple mode): mặc định cho người mới; không giao dịch ký quỹ.
- **Ký quỹ một loại tiền** (single-currency margin): các sản phẩm cùng tiền thanh toán dùng chung ký quỹ và bù trừ lãi lỗ.
- **Ký quỹ đa tiền** (multi-currency margin): dùng chung ký quỹ và bù trừ giữa các vị thế, cả khi tiền thanh toán khác nhau.
- **Ký quỹ danh mục** (portfolio margin): ngoài bù trừ lãi lỗ còn bù trừ rủi ro giữa các phái sinh cùng chỉ số.

Trong mỗi chế độ, vị thế có thể ở dạng **chéo** (cross: chia sẻ ký quỹ trong phạm vi chung) hoặc **cô lập** (isolated: rủi ro của vị thế cô lập được đo riêng và tách khỏi vị thế chéo) [S2]. Muốn đổi chế độ, bạn phải hủy hết lệnh chờ và đóng hết vị thế; chế độ chưa kích hoạt có thể đòi hỏi làm bài kiểm tra kiến thức giao dịch [S2].

**Dễ nhầm về tên gọi**: tài liệu API ghi bốn chế độ là Spot mode, Futures mode, Multi-currency margin mode và Portfolio margin mode, khác tên trên trang Learn [S8][S2]. Khi đọc tài liệu, hãy đối chiếu theo tính năng chứ không theo tên.

Tự tính hệ quả: ký quỹ chéo giúp tận dụng vốn nhưng cũng nghĩa là một vị thế xấu có thể lấy ký quỹ của vị thế khác; bản mô tả của OKX cũng nói rủi ro được đo trên tổng vị thế của tài khoản [S2].

## Hợp đồng vĩnh cửu và funding

**Hợp đồng vĩnh cửu** (perpetual contract, hay perpetual swap) là phái sinh không có ngày hết hạn định sẵn; nó cho phép nắm vị thế mua (long) hoặc bán (short) với tài sản như BTC mà không cần mua bán giao ngay [S3]. Vị thế hợp đồng **không** tương đương số dư giao ngay: lãi lỗ chạy theo quy tắc hợp đồng [S3].

Với hợp đồng tuyến tính (linear) tính và thanh toán bằng USDT, lãi lỗ của vị thế mua là số lượng × (giá đóng − giá vào), và của vị thế bán là số lượng × (giá vào − giá đóng) [S3]. Ví dụ của OKX: mua 0,1 BTC ở 60.000 USDT, đóng ở 61.000 USDT, lãi giá là 0,1 × 1.000 = 100 USDT, chưa tính phí [S3].

**Đòn bẩy** (leverage) đến từ việc ký quỹ thấp hơn giá trị danh nghĩa. Ví dụ trên có giá trị danh nghĩa 6.000 USDT; với 600 USDT vốn ký quỹ, tỷ lệ đơn giản là 10 lần, nhưng lãi lỗ vẫn tính trên 0,1 BTC [S3]. Nền tảng so vốn với yêu cầu duy trì; thua lỗ giá, phí funding hoặc tài sản ký quỹ mất giá có thể khiến lệnh bị hủy, giảm vị thế hoặc thanh lý **mà không chờ mất hết vốn ban đầu** [S3]. Tự tính: ở 10 lần, giá đi ngược khoảng 10% đã xóa gần hết ký quỹ ban đầu, và thanh lý đến sớm hơn mức đó.

Ba loại giá không thay thế nhau: **giá khớp gần nhất** (last) cho thấy hoạt động giao dịch, **giá chỉ số** (index) là tham chiếu giao ngay dùng cho funding, và **giá đánh dấu** (mark) dùng để định giá rủi ro, như lãi lỗ chưa thực hiện và đủ ký quỹ hay chưa [S3].

**Funding** là khoản chuyển giữa bên mua và bên bán để kéo giá hợp đồng về gần giá giao ngay [S4][S5]. Khi tỷ lệ funding dương, bên mua trả bên bán; khi âm, bên bán trả bên mua; nền tảng chỉ tạo điều kiện chuyển tiền và không thu phí dịch vụ trong cơ chế này [S5]. Mặc định funding thanh toán mỗi 8 giờ lúc 00:00, 08:00 và 16:00 UTC, trừ hợp đồng quy định chu kỳ 1, 2 hoặc 4 giờ; bạn chỉ trả hoặc nhận nếu đang giữ vị thế đúng lúc tính [S5].

Công thức của OKX: tỷ lệ funding = kẹp giữa trần và sàn của [chỉ số premium trung bình + kẹp(lãi suất − premium trung bình, ±0,05%)] chia cho (8/N), trong đó lãi suất cố định 0,01% và N là chu kỳ (giờ) [S5]. Premium đo chênh lệch giữa giá khớp ảo hai phía sổ lệnh và giá chỉ số; giá trị khớp ảo bằng 200 lần đòn bẩy tối đa của hợp đồng [S5].

Ví dụ của OKX: vị thế 1.000 USDT, ba lần tính funding với tỷ lệ +0,01%, +0,03%, −0,02%: bên mua trả 0,1 và 0,3 rồi nhận 0,2, ròng trả 0,2 USDT [S4]. Cũng theo OKX, tỷ lệ 0,01% mỗi 8 giờ cộng lại thành 0,03% giá trị vị thế qua ba lần tính trong ngày [S4]. Funding và phí giao dịch là hai dòng tiền riêng [S3].

## Phí giao dịch

Phí giao dịch của OKX theo **bậc**: người dùng thường (Regular) rồi VIP 1 trở lên, phí giảm khi lên bậc [S7]. Trang phí mà phiên viết mở được là bản **OKX Hoa Kỳ** (đường dẫn en-us), và bảng dưới đây là phí giao ngay chuẩn của bản đó [S7]. Bảng ghi phí maker (người đặt lệnh nằm trong sổ) và taker (người khớp ngay với lệnh có sẵn), tính theo tỷ lệ giá trị giao dịch:

| Bậc | Maker | Taker |
|---|---|---|
| Regular | 0,20% | 0,35% |
| VIP 1 | 0,10% | 0,20% |
| VIP 2 | 0,075% | 0,15% |
| VIP 3 | 0,06% | 0,125% |
| VIP 4 | 0,05% | 0,10% |
| VIP 5 | 0,045% | 0,08% |
| VIP 6 | 0,04% | 0,07% |

Trang còn có tab riêng cho cặp stablecoin, nghĩa là cùng một sàn có nhiều bảng phí tùy loại sản phẩm [S7]. Tự tính từ bảng: ở bậc Regular, một lệnh taker 1.000 USD mất 3,5 USD, khứ hồi (mua rồi bán, cả hai taker) mất 7 USD; lệnh maker 1.000 USD mất 2 USD. Phí chỉ là một phần chi phí; funding của hợp đồng vĩnh cửu cộng thêm, như phần trên [S4].

**Đừng hiểu nhầm**: bài **không** nêu phí của bản quốc tế hay bản dành cho Việt Nam. Trang phí toàn cầu không đọc được từ nơi phiên viết chạy (đường dẫn tự chuyển về bản Hoa Kỳ). Một số trang bên thứ ba nêu mức khác, nhưng bài không dùng vì không phải nguồn chính. Hãy mở trang phí của khu vực bạn đang dùng và đối chiếu với bảng ở đây trước khi tin con số nào.

## API và giao dịch tự động

OKX cung cấp API REST và WebSocket cho dữ liệu thị trường và giao dịch; tài liệu bản 5 (v5) nằm ở trang tài liệu chính thức [S8]. Mọi yêu cầu riêng tư phải kèm khóa API, chữ ký và dấu thời gian; máy chủ từ chối yêu cầu lệch quá 30 giây so với giờ máy chủ [S8]. Khi tạo khóa, bạn nhận khóa API, khóa bí mật (secret key) và cụm mật khẩu (passphrase); OKX chỉ lưu bản băm có muối của passphrase nên không khôi phục được nếu bạn làm mất [S8].

Khóa API có ba quyền, gán được một hoặc nhiều: **Read** (xem thông tin, lịch sử), **Trade** (đặt, hủy lệnh, chuyển quỹ, đổi cài đặt) và **Withdraw** (rút tiền) [S8]. Suy luận của người viết: bot chỉ cần đặt lệnh nên chỉ nên được quyền Read và Trade, không cần Withdraw.

Có môi trường **giao dịch thử** (demo trading): dùng tài khoản OKX hiện có, tạo khóa API demo riêng và thêm tiêu đề `x-simulated-trading: 1` vào yêu cầu; một số chức năng như rút, nạp không dùng được [S8]. Giới hạn tốc độ (rate limit) khác nhau theo từng điểm cuối; bị chặn thì nhận mã lỗi 50011; mỗi tài khoản con tối đa 1.000 yêu cầu đặt hoặc sửa lệnh mỗi 2 giây [S8]. Tham số `expTime` cho phép hủy yêu cầu nếu đến máy chủ quá hạn [S8].

## Minh bạch, dự trữ và rủi ro

OKX tuyên bố giữ dự trữ 1:1 cho tài sản trong tài khoản và định kỳ công bố báo cáo **Proof of Reserves** (PoR, bằng chứng dự trữ) [S6]. Báo cáo thứ 49 trên trang ghi 33,87 tỷ USD trên 21 tài sản, trong đó 27,82 tỷ USD là BTC, ETH, USDT và USDC [S6]. Với từng tài sản, trang ghi tỷ lệ dự trữ, ví dụ BTC 108%, ETH 101%, USDT 106% và USDC 100% [S6].

Cách kiểm: OKX dùng cây Merkle và chứng minh không tiết lộ thông tin zk-STARK; người dùng có thể kiểm tra số dư của mình có nằm trong cây, và so tổng tài sản trong ví on-chain của OKX với tổng tài sản tài khoản [S6]. Trang nói rõ báo cáo là **ảnh chụp** tại thời điểm lấy dữ liệu, và phần tài sản ở nhà lưu ký bên thứ ba phải liên hệ nhà lưu ký đó để xác minh [S6].

Giới hạn cần biết: đây là báo cáo do chính OKX công bố, và trong phần văn bản đọc được bài không thấy tên một đơn vị kiểm toán độc lập [S6]. Suy luận của người viết: PoR cho biết tài sản không thấp hơn số dư tài khoản vào một thời điểm; nó không thay thế giấy phép, kiểm toán độc lập hay bảo đảm về thanh khoản và vận hành.

Các rủi ro cụ thể rút ra từ các nguồn: **thanh lý** khi ký quỹ không đủ [S3]; **funding** làm giảm ký quỹ khi bạn ở phía trả [S3][S4]; **phí** theo bậc [S7]; **sản phẩm và quy tắc khác nhau theo khu vực** [S5][S7]; **tiền sử sự cố**, gồm thanh lý với thu hồi lãi 17% năm 2018 và ngừng rút tiền năm 2020 [S1].

## Cách dùng OKX có kỷ luật

Đây là phần **suy luận của người viết**, dựa trên các nguồn ở trên, không phải khuyến nghị đầu tư. Một quy trình thận trọng gồm sáu bước.

1. **Xác định pháp nhân và khu vực của bạn**: sản phẩm và phí khác nhau theo khu vực [S5][S7]. Bài chưa xác minh OKX có được cấp phép hay phục vụ người ở Việt Nam hay không; hãy tự kiểm tra trước khi nạp tiền.
2. **Chọn chế độ tài khoản tối thiểu cần thiết**: mặc định chế độ đơn giản không có ký quỹ [S2]; chỉ nâng khi bạn hiểu chế độ đó.
3. **Đọc thông số hợp đồng**: đơn vị số lượng, tiền thanh toán, tiền ký quỹ, quy tắc funding và thanh lý [S3].
4. **Tính tổng chi phí**: phí maker hoặc taker [S7] cộng funding nếu giữ vị thế qua các mốc tính [S4].
5. **Thử trên demo trước khi dùng tiền thật hoặc bot**, và cấp khóa API quyền tối thiểu [S8].
6. **Coi PoR là một lớp thông tin, không phải bảo hiểm** [S6].

## Điều cần nhớ

OKX là một nền tảng, không phải một sản phẩm: giao ngay, ký quỹ, hợp đồng vĩnh cửu, kỳ hạn và quyền chọn dùng chung một hệ tài khoản [S8][S2]. Đòn bẩy làm khuếch đại cả lãi lẫn lỗ và có thể dẫn đến thanh lý trước khi mất hết vốn [S3]. Funding là dòng tiền riêng giữa bên mua và bên bán, mặc định mỗi 8 giờ [S5]. Phí và sản phẩm phụ thuộc khu vực: đối chiếu trang chính thức của khu vực bạn dùng [S7]. PoR hữu ích nhưng do chính sàn công bố [S6].

## Lưu ý

Bài này **không phải lời khuyên tài chính hay đầu tư**. Giao dịch tiền mã hóa, nhất là có đòn bẩy, có thể làm mất toàn bộ số vốn; chính OKX cảnh báo rằng nội dung Learn chỉ mang tính thông tin và có thể nói đến sản phẩm không có ở khu vực của bạn [S2].

Giới hạn nguồn của bài, đọc trước khi tin các con số:

- Phiên viết chạy từ một nơi mà trang phí toàn cầu tự chuyển về bản Hoa Kỳ, nên mọi con số phí là của bản Hoa Kỳ [S7]; bài không biết phí bản dành cho bạn.
- Chỉ có một nguồn ngoài OKX là Wikipedia [S1]. Bài chưa đọc được đánh giá độc lập nào của bên thứ ba có thể mở được.
- Kết quả tìm kiếm cho thấy có một vụ việc giữa OKX và cơ quan tư pháp Hoa Kỳ năm 2025, nhưng trang thông cáo gốc trả về nội dung rỗng khi đọc, nên bài **không** dùng làm nguồn và không nêu chi tiết. Nếu bạn cân nhắc dùng OKX, hãy tự tìm và đọc nguồn này.
- Bài không xác minh tình trạng cấp phép của OKX ở Việt Nam.
- Số liệu Proof of Reserves, phí và sản phẩm đổi theo thời gian; các con số tính đến ngày 12/11/2026.

## Nguồn tham khảo

- [S1] [Wikipedia, OKX](https://en.wikipedia.org/wiki/OKX)
- [S2] [OKX Learn, What is a unified account?](https://www.okx.com/en-us/learn/what-is-a-unified-account)
- [S3] [OKX Learn, What is a perpetual contract?](https://www.okx.com/en-us/learn/what-is-perpetual-swap)
- [S4] [OKX Learn, What is a funding rate?](https://www.okx.com/en-us/learn/what-is-funding-rate)
- [S5] [OKX Help, Perpetual futures funding fee mechanism](https://www.okx.com/en-us/help/perps-funding-fee-mechanism)
- [S6] [OKX, Proof of Reserves](https://www.okx.com/en-us/proof-of-reserves)
- [S7] [OKX Hoa Kỳ, Trading fee (bảng phí và menu sản phẩm)](https://www.okx.com/en-us/fees)
- [S8] [OKX, API Guide v5 (tài liệu API)](https://www.okx.com/docs-v5/en/)
