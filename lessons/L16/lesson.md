---
id: L16
title: Grok Bot: đội agent AI chạy trên máy tính đám mây
topic: ky-thuat
date: 2026-10-21
---
# Grok Bot: đội agent AI chạy trên máy tính đám mây

## Tóm tắt

Grok Bot có đáng tiền không, rủi ro ở đâu, và việc gì nên giao cho nó? Câu trả lời ngắn: Grok Bot là sản phẩm agent AI của xAI, ra mắt dạng thử nghiệm sớm (early beta) ngày 11/08/2026. Mỗi lần giao việc, một Bot làm trên một máy tính đám mây có trình duyệt, hệ thống file và terminal, nên nó vẫn chạy khi người dùng đã tắt laptop [S8] [S9] [S10]. Giá trị lớn nhất nằm ở **việc lặp lại theo lịch**; nhược điểm lớn nhất là các Bot của cùng một người dùng **dùng chung một máy**, và giá, gói truy cập, nền tảng còn đổi nhanh (suy luận của người viết, tổng hợp từ [S5] [S9] [S11]).

Bài này đọc Grok Bot theo năm câu hỏi: nó là gì và hoạt động ra sao; giao việc bằng cách nào; tốn bao nhiêu tiền; mạnh và yếu ở đâu; và hệ sinh thái cùng các use case thực tế. Mỗi khẳng định được gắn mức chắc chắn: **nguồn chính thức** (tài liệu của xAI hoặc Cursor), **nguồn thứ ba** (blog, báo, so sánh), **mâu thuẫn** (các nguồn nói khác nhau) hoặc **suy luận của người viết**.

Ba ý đáng mang theo. Thứ nhất, Grok Bot không phải chatbot trả lời một câu; nó là một "đồng đội" nhận việc, tự thao tác trên máy đám mây rồi báo lại [S8] [S9]. Thứ hai, "mỗi Bot một máy riêng" và "mọi Bot của một người dùng chung một máy" là hai mô tả mâu thuẫn trong các nguồn; tài liệu bảo mật của Cursor nói rõ là dùng chung [S5] [S7]. Thứ ba, đừng tin con số giá nào mà chưa đối chiếu với trang giá hiện hành: các nguồn không thống nhất [S10] [S11] [S15].

## Grok Bot là gì

**Tên gọi (nguồn thứ ba).** "Grok Bot" ở đây là sản phẩm agent của xAI. Bài báo Gigazine đưa tin ra mắt dưới tên SpaceXAI và mô tả đây là agent AI làm việc 24 giờ [S7].

**Ra mắt và trạng thái (nguồn thứ ba, nhiều nguồn khớp).** Sản phẩm ra mắt bản beta ngày 11/08/2026 và vẫn được gọi là "early beta" ở các bài tháng 9 [S8] [S9] [S10]. Chữ beta có nghĩa thực tế: tính năng, gói truy cập và nền tảng thay đổi trong vài tuần, như phần chi phí bên dưới cho thấy.

**Bot khác chatbot ở đâu (nguồn thứ ba).** Một chatbot trả lời khi bạn hỏi và dừng lại. Một Bot nhận một công việc, dùng trình duyệt, file và terminal trên máy đám mây để làm, có thể đăng nhập vào ứng dụng của bạn, và tiếp tục khi bạn không còn ngồi trước máy [S8] [S9]. Alarcon, người dùng thử trả phí một tuần, gói gọn thành quy tắc: Grok Bot hợp với **việc đứng chờ theo lịch**, không hợp với câu hỏi một lần [S9].

**Mô hình nền (nguồn thứ ba).** Theo các tóm tắt của tài liệu xAI và Cursor, Bot chạy trên Grok 4.6 và người dùng không tự chọn mô hình [S1] [S4]. Mem0 mô tả thêm kho công cụ đi kèm: trình duyệt, file, terminal, plugin và MCP connector, nhiều Bot phối hợp, và cổng phê duyệt cho hành động nhạy cảm [S8].

## Cách hoạt động: máy tính đám mây và các Bot

**Máy tính đám mây (nguồn chính thức).** Tài liệu của Cursor nói rõ: mỗi người dùng có một máy ảo riêng chạy trên Firecracker microVM, với nhân hệ điều hành, bộ nhớ và thiết bị ảo riêng; người dùng này không vào được máy của người dùng khác [S5].

**Điểm hay bị hiểu nhầm: máy riêng cho mỗi người, không phải cho mỗi Bot (mâu thuẫn).** Tài liệu Cursor và xAI cho biết mọi Bot của cùng một người dùng **dùng chung một máy**; mỗi Bot có màn hình riêng để làm việc song song, nhưng đó là bề mặt làm việc, không phải ranh giới bảo mật [S4] [S5]. Trong khi đó tiêu đề tin Gigazine nói mỗi agent điều khiển một PC đám mây riêng [S7], và Mem0 viết mỗi Bot có trình duyệt, file và terminal của nó [S8]. Suy luận của người viết: các bài này mô tả theo cảm nhận người dùng, còn tài liệu bảo mật mô tả kiến trúc, nên khi hai bên lệch nhau thì theo tài liệu bảo mật [S5].

**Chỉ chạy trên hạ tầng của Cursor (nguồn chính thức).** Grok Bot hiện chỉ chạy trên máy đám mây do Cursor lưu trữ; chưa hỗ trợ triển khai tại chỗ (on-premises), trong vành đai riêng của doanh nghiệp, hay tự mang image [S5].

**Phiên đăng nhập có thể mất (nguồn chính thức).** Khi máy đám mây được tạo lại, ví dụ sau cập nhật image hoặc đổi chính sách, các phiên đăng nhập bên trong có thể rơi [S5]. Hệ quả thực tế: việc định kỳ có thể đột nhiên đòi đăng nhập lại.

**Nhiều Bot, một đầu việc (nguồn chính thức).** Khi tạo chat mới, người dùng chọn từ hai đến sáu Bot để lập thành một nhóm cùng chia sẻ một kết quả; các Bot đăng vào nhóm và chuyển việc cho nhau [S2].

## Giao việc cho Bot: chat, nhóm, routine và kết nối

**Chat và điều khiển giữa chừng (nguồn chính thức).** Trong khung chat, bạn gõ @ để nhắc một Bot, một nhóm, một routine hoặc một connector, và gõ / để gọi kỹ năng đã lưu. Bạn có thể gửi chỉ dẫn mới khi Bot đang làm. Lệnh "Stop now" dừng công việc nhưng **không hoàn tác** những gì đã làm xong [S2]. Bản ghi hội thoại hiện cả hoạt động công cụ, thao tác máy tính, file đã tạo, câu hỏi của Bot và các yêu cầu phê duyệt [S2].

**Nhóm và @everyone (nguồn chính thức).** Trong nhóm, @ một Bot để giao riêng, nhắc nhiều Bot để giao nhiều người, hoặc @everyone để gọi tất cả [S2].

**Phê duyệt (nguồn chính thức và nguồn thứ ba).** Với hành động nhạy cảm, Bot dừng lại hỏi. Các lựa chọn được mô tả là Allow once, Deny và Always allow, cộng với luật Auto Review: hoặc dừng chờ người ký, hoặc tự chạy khi thỏa điều kiện đã đặt [S3] [S16]. Ứng dụng iOS cho phép duyệt từng bước khi bạn không ở bàn làm việc [S2] [S14]. Một hướng dẫn kỹ năng khuyên bắt buộc phê duyệt trước khi gửi, đăng, mua, xóa, đổi quyền hoặc sản phẩm đang chạy, và trước khi chấp nhận điều khoản pháp lý [S18].

**Routine (nguồn chính thức).** Routine là việc lặp lại theo lịch hoặc theo sự kiện. Người dùng có thể lập alias email, rồi tạo routine chạy mỗi khi có thư tới địa chỉ đó [S2].

**Connector (nguồn chính thức và nguồn thứ ba).** Danh sách connector dựng sẵn gồm Microsoft Teams (tin nhắn, kênh, hội thoại), Salesforce và SharePoint, ngoài ra có danh mục connector bên thứ ba [S2] [S13]. Một bài tháng 9/2026 mô tả connector Teams tìm kiếm, đọc và gửi tin nhắn trong hội thoại và kênh [S13]. Một bài tháng 10/2026 nói bản cập nhật lớn thêm chợ connector để các nhóm tự nộp tích hợp của mình, và hỗ trợ X Chat [S14].

**Bộ nhớ (nguồn thứ ba, một nguồn).** Một bài so sánh ghi rằng Cursor chưa có tài liệu nói cách xem hay sửa bộ nhớ của Grok Bot, trong khi OpenClaw và Hermes lưu bộ nhớ thành file văn bản có thể sửa [S12].

## Chi phí và gói truy cập

**Không có giá riêng (nguồn thứ ba, nhiều nguồn khớp).** Grok Bot không bán lẻ; quyền dùng nằm trong gói đăng ký khác. Từ lúc ra mắt đến nay gói được phép dùng đã đổi: ngày ra mắt chỉ các gói cao nhất, ngày 26/08/2026 mở cho mọi gói SuperGrok, Cursor Pro và Cursor Teams [S11] [S15].

**Con số giá (mâu thuẫn).** Bảng dưới gom lại, kèm nguồn. Đây là điểm các nguồn lệch nhau nhiều nhất.

| Gói | Giá được nêu | Nguồn | Mức chắc chắn |
|---|---|---|---|
| SuperGrok cơ bản | khoảng $30 mỗi tháng | [S9] [S11] [S15] | nhiều nguồn khớp, chưa kiểm trang giá |
| SuperGrok Plus | khoảng $100 mỗi tháng | [S11] [S15] | một nhóm nguồn |
| SuperGrok Heavy | khoảng $300 mỗi tháng | [S11] [S15] | có nguồn nói đây là yêu cầu lúc ra mắt; Alarcon nói yêu cầu này không còn đúng [S9] |
| Cursor Pro | khoảng $20 mỗi tháng | [S12] | một bài so sánh; tài liệu xAI có thể liệt kê hẹp hơn |
| Cursor Ultra | khoảng $200 mỗi tháng | [S10] | một nguồn; chưa có nguồn thứ hai xác nhận |

**Mâu thuẫn về danh sách gói.** Một bài tổng hợp ghi rằng trang FAQ của xAI vẫn liệt kê một tập gói hẹp hơn, bắt đầu từ Cursor Pro+, trong khi các nguồn khác nói mọi gói Cursor Pro đều có [S11]. Suy luận của người viết: chưa thể kết luận gói nào "đủ" nếu chưa mở trang giá chính thức vào đúng ngày mua.

**Dùng thử và hạn mức (nguồn chính thức và nguồn thứ ba).** Cursor mô tả dùng thử là một khoản tín dụng sử dụng trong cửa sổ bảy ngày; phần đã dùng không được hoàn lại, và một tác vụ lớn có thể dùng hết [S6]. Một nguồn khác ghi bảy ngày và phải nhập thẻ trước [S10]; nguồn khác ghi mười bốn ngày [S11]. Các gói trả phí có hạn mức hằng tuần nhưng mức cụ thể không được công bố, và xAI không nêu trần chi riêng cho Grok Bot, dù các kiểm soát chi tiêu cấp tài khoản vẫn áp dụng [S6] [S11].

**Bản doanh nghiệp.** Một bài chụp trang giá ngày 10/09/2026 ghi Grok Bot chưa nằm trong gói Business hay Enterprise [S9]. Cursor ghi Team Setup chỉ dành cho Enterprise [S5].

## Ưu điểm

**Làm việc nền, không cần laptop (nguồn thứ ba).** Đây là điểm khác biệt nhất: việc theo lịch chạy tiếp khi bạn tắt máy [S8] [S9].

**Hành động trên công cụ thật (nguồn thứ ba).** Có trình duyệt, file và terminal nên Bot làm được việc như kiểm tra trang web, điền biểu mẫu, chạy lệnh, tạo file, chứ không chỉ trả lời văn bản [S8].

**Song song và phối hợp (nguồn chính thức).** Hai đến sáu Bot trong một nhóm, cùng nhận một đầu việc và chuyển việc cho nhau [S2].

**Có cổng kiểm soát (nguồn chính thức).** Allow once, Deny, Always allow và Auto Review cho phép giữ con người trong vòng lặp với việc nhạy cảm, và tự động với việc lặp lại an toàn [S3] [S16].

**Cô lập giữa người dùng (nguồn chính thức).** Mỗi người một microVM với nhân riêng; người này không với tới máy của người kia [S5].

**Kết nối rộng (nguồn thứ ba).** Teams, Salesforce, SharePoint, chợ connector và MCP giúp Bot nối vào công cụ có sẵn của tổ chức [S2] [S8] [S14].

## Nhược điểm và rủi ro bảo mật

**Mọi Bot của một người dùng chung một máy (nguồn chính thức).** Cursor khuyến cáo coi mọi đăng nhập và file trên máy là có thể dùng được bởi mọi Bot của người đó; màn hình của từng Bot không phải ranh giới bảo mật [S4] [S5]. Vellum cũng chỉ ra rằng các Bot có thể truy cập cùng một phiên trình duyệt đã đăng nhập [S16]. Cách giảm thiểu được khuyến nghị: quyền tối thiểu, giao thông tin đăng nhập thủ công, luật phê duyệt hẹp và thu hồi quyền ở phía nguồn [S5] [S16].

**Phiên đăng nhập có thể rơi (nguồn chính thức).** Máy đám mây được tạo lại sau cập nhật image hoặc đổi chính sách, và các phiên bên trong mất theo [S5].

**Chỉ trên hạ tầng Cursor, thiếu công cụ quản trị (nguồn chính thức).** Chưa có on-premises hay image tự mang; không có sẵn nguồn dữ liệu EDR cho khách hàng; Team Setup chỉ ở Enterprise [S5]. Một hướng dẫn nói thiếu màn hình kiểm toán đầy đủ mọi hành động của Bot [S16].

**Còn beta, giá và nền tảng đổi liên tục (nguồn thứ ba).** Gói được dùng đã đổi trong hai tuần đầu; nền tảng cũng bị mô tả khác nhau, một nguồn nói bản đầu chỉ có trên macOS Apple Silicon, tiêu đề Gigazine nêu cả Windows, macOS, Linux và iOS [S7] [S10].

**Thao tác trên trang đã đăng nhập chưa trơn tru (nguồn thứ ba, một thử nghiệm).** Mem0 thấy tác vụ trình duyệt trên trang công khai chạy được, còn chụp màn hình trang cần đăng nhập có thể đòi đăng nhập thêm [S8].

**Khó dự đoán chi phí sử dụng (nguồn chính thức).** Hạn mức hằng tuần không công bố và một tác vụ lớn có thể dùng hết khoản dùng thử [S6]. Suy luận của người viết: chạy nhiều Bot liên tục khó ước chi phí trước.

**Không chọn được mô hình (nguồn thứ ba).** Theo tóm tắt tài liệu, Bot chạy Grok 4.6 và người dùng không đổi được [S1] [S4].

## Hệ sinh thái

**xAI (SpaceXAI) và dòng mô hình Grok.** Bên làm sản phẩm; Gigazine gọi bên phát hành là SpaceXAI [S7]. Tài liệu chính thức nằm ở docs.x.ai, gồm FAQ, chat và cộng tác, bảo mật [S1] [S2] [S3].

**Cursor.** Bên lưu trữ máy đám mây và có tài liệu riêng (bắt đầu, bảo mật, trợ giúp); Cursor Pro và Cursor Teams là hai đường vào [S4] [S5] [S6].

**SuperGrok.** Đường vào trực tiếp từ xAI với các bậc giá khác nhau [S11] [S15].

**Ứng dụng.** Ứng dụng iOS để duyệt và xem kết quả khi vắng bàn; một nguồn mô tả bản đầu trên macOS, nguồn khác thêm Windows [S7] [S10] [S14].

**Connector và routine.** Teams, Salesforce, SharePoint, danh mục bên thứ ba, chợ connector, MCP; email alias kích hoạt routine [S2] [S8] [S13] [S14].

**Hệ phụ trợ bên thứ ba.** Mem0, Vellum, Alarcon, Toolradar và nhiều blog viết hướng dẫn và đánh giá [S8] [S9] [S12] [S16] [S17]. Đây là phân tích, không phải tài liệu chính thức; nên đối chiếu khi một chi tiết quan trọng.

## Use case thực tế

**Khung chọn việc (nguồn thứ ba).** Alarcon đặt ba phép thử: việc lặp lại theo lịch; chạy được mà không cần file trên laptop; kết quả để lại cho bạn kiểm tra sau. Trượt một phép thử thì đó không phải việc của Bot [S9].

**Việc được nêu trong các bài đánh giá (nguồn thứ ba).** Mem0 liệt kê: theo dõi đối thủ cạnh tranh, kiểm tra kho mã, nghiên cứu nhiều nguồn song song, sinh mã, xác minh dữ kiện, lập kịch bản [S8].

**Ví dụ vận hành (nguồn thứ ba).** Toolradar mô tả một Bot quản lý chi phí chỉ soạn tóm tắt và nhắc việc, không đổi số liệu hoàn chi [S17].

**Áp dụng khung cho ba tình huống (suy luận của người viết, không phải kết quả đã kiểm).**

1. Mỗi sáng tóm tắt thay đổi trang giá và changelog của ba đối thủ: lặp lại, không cần file cục bộ, đọc kết quả sau. Đạt cả ba phép thử [S9].
2. Mỗi tuần quét repository để tìm dependency lỗi thời và issue cũ rồi tóm tắt: lặp lại, phụ thuộc kho trên đám mây. Đạt, nếu cấp quyền chỉ đọc [S8] [S18].
3. Một câu hỏi pháp lý hỏi một lần cần câu trả lời ngay: không lặp lại, không phải việc của Bot; dùng chatbot thường [S9].

## So sánh với agent tự dựng

**Hai cực của agent cá nhân (nguồn thứ ba).** Toolradar đặt Grok Bot ở cực quản lý trả phí: nhà cung cấp lo máy chủ, chạy trên đám mây của Cursor, từ khoảng $20 mỗi tháng. OpenClaw ở cực tự dựng: mã nguồn mở, miễn phí bản thân phần mềm, nhưng bạn tự cấp máy chủ và trả tiền mô hình [S12].

| Tiêu chí | Grok Bot | OpenClaw (tự dựng) |
|---|---|---|
| Ai lo máy chạy | nhà cung cấp [S12] | bạn [S12] |
| Chi phí | gói đăng ký [S12] | máy chủ và mô hình [S12] |
| Bộ nhớ | chưa có tài liệu xem hoặc sửa [S12] | file văn bản sửa được [S12] |
| Rủi ro ghi nhận | máy dùng chung giữa các Bot [S5] | chợ kỹ năng từng có chiến dịch mã độc [S12] |

**Giới hạn của phép so sánh.** Kết quả tìm kiếm không có bài nào so Grok Bot với các agent chạy trên Claude, nên bài này không so sánh với chúng (suy luận của người viết).

## Có nên dùng không

**Nên thử khi** bạn có việc theo lịch cần chạy khi máy đã tắt; chấp nhận rằng mọi đăng nhập trên máy đám mây là chung cho các Bot của mình; bắt đầu bằng tài khoản và dữ liệu không nhạy cảm [S5] [S9].

**Chưa nên khi** bạn cần cách ly bảo mật giữa các tác vụ; cần triển khai trong hạ tầng riêng hoặc yêu cầu tuân thủ chặt; hoặc cần chi phí ổn định và dự đoán được [S5] [S6].

**Quy trình thử gợi ý (suy luận của người viết).** Chọn một việc đạt ba phép thử của Alarcon; chỉ cấp quyền tối thiểu; đặt phê duyệt cho mọi hành động ra ngoài như gửi thư, mua hàng, xóa; xem bản ghi sau vài lần chạy rồi mới mở rộng; thu hồi quyền ở phía nguồn khi ngừng dùng [S5] [S9] [S18].

## Điều cần nhớ

Bốn ý. Một: Grok Bot là agent chạy nền trên máy tính đám mây, mạnh ở việc lặp lại theo lịch [S8] [S9]. Hai: các Bot của một người dùng chung một máy, nên đừng coi đó là cách ly [S5]. Ba: giá và gói truy cập chưa ổn định và các nguồn lệch nhau, hãy kiểm trang giá hiện hành [S11] [S15]. Bốn: đặt phê duyệt cho hành động ra ngoài và cấp quyền tối thiểu [S3] [S18].

## Lưu ý

Bài này **không phải lời khuyên tài chính hay bảo mật** cho một tổ chức cụ thể. Giới hạn của bài: tài liệu chính thức của xAI và Cursor được dẫn ở đây qua bản tóm tắt của công cụ tìm kiếm chứ chưa được đọc toàn văn trong phiên viết bài, nên các chi tiết đáng tiền (giá, gói, nền tảng, hạn mức) cần đối chiếu trực tiếp trước khi quyết định. Bài đã bỏ một thông tin về việc bán qua một gói đăng ký khác từ tháng 10/2026 vì chỉ có một nguồn không xác định được. Sản phẩm còn beta; nội dung phản ánh tình hình đến ngày 21/10/2026.

## Nguồn tham khảo

- [S1] xAI, Grok Bot FAQ (tài liệu), 2026, https://docs.x.ai/grok-bot/faq
- [S2] xAI, Work with Grok Bot: chat và cộng tác (tài liệu), 2026, https://docs.x.ai/grok-bot/chat-and-collaboration
- [S3] xAI, Manage and protect: bảo mật Grok Bot (tài liệu), 2026, https://docs.x.ai/grok-bot/security-faq
- [S4] Cursor, Get started with Grok Bot (tài liệu), 2026, https://cursor.com/docs/grok-bot/get-started
- [S5] Cursor, Grok Bot security FAQ (tài liệu), 2026, https://cursor.com/docs/grok-bot/security-faq
- [S6] Cursor, Grok Bot FAQs (trợ giúp), 2026, https://cursor.com/help/grok-bot/faqs
- [S7] Gigazine, SpaceXAI ra mắt agent AI Grok Bot (tin), 12/08/2026, https://gigazine.net/gsc_news/en/20260812-spacexai-grok-bot/
- [S8] Mem0, Grok Bot guide: pricing, features and setup, 2026, https://mem0.ai/blog/grok-bot-guide
- [S9] Christopher Alarcon, Grok Bot use cases: the 12 jobs I actually run, 2026, https://christopheralarcon.com/blog/grok-bot-use-cases
- [S10] MindStudio, Grok Bot pricing and access, 2026, https://www.mindstudio.ai/blog/grok-bot-pricing-access/
- [S11] AI Builder Club, Grok Bot pricing 2026: plans, usage limits, free trial, platforms, 2026, https://www.aibuilderclub.com/blog/grok-bot-pricing
- [S12] Toolradar, OpenClaw vs Grok Bot, 2026, https://toolradar.com/compare/openclaw-vs-grok-bot
- [S13] Tesla North, Grok Bot can search and act across Microsoft Teams, 11/09/2026, https://teslanorth.com/2026/09/11/grok-bot-microsoft-teams
- [S14] iPhone in Canada, Grok Bot gets major update with new features and X Chat support, 17/10/2026, https://www.iphoneincanada.ca/2026/10/17/grok-bot-major-update/
- [S15] ColdICP, Grok Bot pricing: every plan from $20 to $300 a month, 2026, https://coldicp.com/grok-bot-pricing/
- [S16] Vellum, Official Grok Bot breakdown, 2026, https://www.vellum.ai/blog/official-grok-bot-breakdown
- [S17] Toolradar, Grok Bot use cases, 2026, https://toolradar.com/blog/grok-bot-use-cases
- [S18] skills.sh, grok-bot (hướng dẫn kỹ năng), 2026, https://www.skills.sh/andrueandersoncs/skills/grok-bot
