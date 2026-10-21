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

Ba ý đáng mang theo. Thứ nhất, Grok Bot không phải chatbot trả lời một câu; nó là một "đồng đội" nhận việc, tự thao tác trên máy đám mây rồi báo lại [S8] [S9]. Thứ hai, "mỗi Bot một máy riêng" và "mọi Bot của một người dùng chung một máy" là hai mô tả mâu thuẫn trong các nguồn; tài liệu bảo mật của Cursor nói rõ là dùng chung [S5] [S7]. Thứ ba, đừng tin con số giá nào mà chưa đối chiếu với trang giá hiện hành: các nguồn không thống nhất [S10] [S11].

## Grok Bot là gì

**Tên gọi (nguồn thứ ba).** "Grok Bot" ở đây là sản phẩm agent của xAI. Bài báo Gigazine đưa tin ra mắt dưới tên SpaceXAI và mô tả đây là agent AI làm việc 24 giờ [S7].

**Ra mắt và trạng thái (nguồn thứ ba, nhiều nguồn khớp).** Sản phẩm ra mắt bản beta ngày 11/08/2026 và vẫn được gọi là "early beta" ở các bài tháng 9 [S8] [S9] [S10]. Chữ beta có nghĩa thực tế: tính năng, gói truy cập và nền tảng thay đổi trong vài tuần, như phần chi phí bên dưới cho thấy.

**Bot khác chatbot ở đâu (nguồn thứ ba).** Một chatbot trả lời khi bạn hỏi và dừng lại. Một Bot nhận một công việc, dùng trình duyệt, file và terminal trên máy đám mây để làm, có thể đăng nhập vào ứng dụng của bạn, và tiếp tục khi bạn không còn ngồi trước máy [S8] [S9]. Alarcon, người dùng thử trả phí một tuần, gói gọn thành quy tắc: Grok Bot hợp với **việc đứng chờ theo lịch**, không hợp với câu hỏi một lần [S9].

**Mô hình nền (nguồn chính thức).** Grok Bot không gắn với một mô hình cố định và không có bộ chọn mô hình: với mỗi tác vụ, dịch vụ dùng mô hình được cho là cho kết quả tốt nhất, của xAI hoặc của một nhà cung cấp bên thứ ba nằm trong danh sách nhà xử lý phụ (sub-processor); tập mô hình đổi theo thời gian [S15]. Cursor ghi rằng danh sách cho phép mô hình (allowlist) của nhóm không chi phối Grok Bot [S15]; tài liệu xAI mới hơn có thể mô tả khác, điều chưa đối chiếu được trong phiên viết bài. Vì vậy ai quan tâm nhà cung cấp nào có thể xử lý dữ liệu đã kết nối cần xem danh sách nhà xử lý phụ, không suy ra từ một tên mô hình. Mem0 mô tả thêm kho công cụ đi kèm: trình duyệt, file, terminal, plugin và MCP connector, nhiều Bot phối hợp, và các cổng phê duyệt cho hành động nhạy cảm [S8].

## Cách hoạt động: máy tính đám mây và các Bot

**Máy tính đám mây (nguồn chính thức).** Tài liệu của Cursor nói rõ: mỗi người dùng có một máy ảo riêng chạy trên Firecracker microVM, với nhân hệ điều hành, bộ nhớ và thiết bị ảo riêng; người dùng này không vào được máy của người dùng khác [S5].

**Điểm hay bị hiểu nhầm: máy riêng cho mỗi người, không phải cho mỗi Bot (mâu thuẫn).** Tài liệu Cursor và xAI cho biết mọi Bot của cùng một người dùng **dùng chung một máy**; mỗi Bot có màn hình riêng để làm việc song song, nhưng đó là bề mặt làm việc, không phải ranh giới bảo mật [S4] [S5]. Trong khi đó tiêu đề tin Gigazine nói mỗi agent điều khiển một PC đám mây riêng [S7], và Mem0 viết mỗi Bot có trình duyệt, file và terminal của nó [S8]. Suy luận của người viết: các bài này mô tả theo cảm nhận người dùng, còn tài liệu bảo mật mô tả kiến trúc, nên khi hai bên lệch nhau thì theo tài liệu bảo mật [S5].

**Chỉ chạy trên hạ tầng của Cursor (nguồn chính thức).** Grok Bot hiện chỉ chạy trên máy đám mây do Cursor lưu trữ; chưa hỗ trợ triển khai tại chỗ (on-premises), trong vành đai riêng của doanh nghiệp, hay tự mang image [S5].

**Phiên đăng nhập có thể mất (nguồn chính thức).** Khi máy đám mây được tạo lại, ví dụ sau cập nhật image hoặc đổi chính sách, các phiên đăng nhập bên trong có thể rơi [S5]. Hệ quả thực tế: việc định kỳ có thể đột nhiên đòi đăng nhập lại.

**Nhiều Bot, một đầu việc (nguồn chính thức).** Khi tạo chat mới, người dùng chọn từ hai đến sáu Bot để lập thành một nhóm cùng chia sẻ một kết quả; các Bot đăng vào nhóm và chuyển việc cho nhau [S2].

## Giao việc cho Bot: chat, nhóm, routine và kết nối

**Chat và điều khiển giữa chừng (nguồn chính thức).** Trong khung chat, bạn gõ @ để nhắc một Bot, một nhóm, một routine hoặc một connector, và gõ / để gọi kỹ năng đã lưu. Bạn có thể gửi chỉ dẫn mới khi Bot đang làm. Lệnh "Stop now" dừng công việc nhưng **không hoàn tác** những gì đã làm xong [S2]. Bản ghi hội thoại hiện cả hoạt động công cụ, thao tác máy tính, file đã tạo, câu hỏi của Bot và các yêu cầu phê duyệt [S2].

**Nhóm và @everyone (nguồn chính thức).** Trong nhóm, @ một Bot để giao riêng, nhắc nhiều Bot để giao nhiều người, hoặc @everyone để gọi tất cả [S2].

**Phê duyệt: cấu hình được, không phải bảo đảm (nguồn chính thức).** Các lựa chọn khi Bot xin phép được mô tả là Allow once, Deny và Always allow, cộng với luật Auto Review [S3] [S16]. Nhưng việc Bot có dừng hỏi hay không phụ thuộc vào công cụ, mức rủi ro của hành động và cấu hình Auto Review [S1]. Auto Review là một mô hình độc lập kiểm tra trước các hành động rủi ro (lệnh shell, gọi plugin, thao tác máy tính, ghi vào automation, giao việc) và có thể cho chạy, yêu cầu duyệt hoặc chặn; nó không xem xét mọi tác dụng phụ, ví dụ ghi bộ nhớ và phần lớn thay đổi cài đặt [S18]. Luật Ask first luôn dừng các hành động khớp luật; luật Allow automatically chỉ cho chạy khi bộ kiểm tra không thấy lý do khác để dừng [S18]. Khóa để thành viên không tắt được Auto Review chỉ có ở Enterprise và mặc định tắt [S18]. Các biện pháp này giảm chứ không loại bỏ rủi ro từ nội dung độc hại như trang web hay kết quả lệnh (prompt injection) [S18]. Vì vậy, trước khi cấp quyền ghi cho Bot (gửi tin, xóa dữ liệu, mua hàng), hãy đặt luật Ask first cho đúng các hành động đó và coi phê duyệt là một lớp bảo vệ bên cạnh quyền tối thiểu, không phải ranh giới đã được chứng minh [S18]. Ứng dụng iOS cho phép duyệt từng bước khi bạn không ở bàn làm việc [S2] [S14].

**Routine (nguồn chính thức).** Routine là việc lặp lại theo lịch hoặc theo sự kiện. Người dùng có thể lập alias email, rồi tạo routine chạy mỗi khi có thư tới địa chỉ đó [S2].

**Connector (nguồn chính thức và nguồn thứ ba).** Danh sách connector dựng sẵn gồm Microsoft Teams (tin nhắn, kênh, hội thoại), Salesforce và SharePoint, ngoài ra có danh mục connector bên thứ ba [S2] [S13]. Một bài tháng 9/2026 mô tả connector Teams tìm kiếm, đọc và gửi tin nhắn trong hội thoại và kênh [S13]. Một bài tháng 10/2026 nói bản cập nhật lớn thêm chợ connector để các nhóm tự nộp tích hợp của mình, và hỗ trợ X Chat [S14].

**Bộ nhớ (nguồn thứ ba, một nguồn).** Một bài so sánh ghi rằng Cursor chưa có tài liệu nói cách xem hay sửa bộ nhớ của Grok Bot, trong khi OpenClaw và Hermes lưu bộ nhớ thành file văn bản có thể sửa [S12].

## Chi phí và gói truy cập

**Không có giá riêng: quyền dùng đi kèm gói khác (nguồn chính thức).** Grok Bot không bán lẻ. Tài liệu gói và thanh toán của Cursor phân biệt các đường truy cập sau; đây là trang mới hơn các bài viết tháng 8 và 9, và bản sao cũ hơn của chính trang đó chưa nhắc The X Subscription [S17].

1. **The X Subscription.** Các bậc Premium, Super và Ultra có Grok Bot, cho cá nhân và cho chỗ ngồi nhóm; bậc Plus và Free thì không [S17].
2. **Gói Cursor cũ (legacy).** Pro, Pro+ và Ultra có Grok Bot; một chỗ Teams tự phục vụ cấp quyền cho mọi thành viên, không cần mua riêng [S17].
3. **Liên kết tài khoản.** Tài khoản cá nhân SuperGrok, SuperGrok Plus, SuperGrok Heavy hoặc X Premium+ có thể liên kết với tài khoản Cursor cũ để cấp lượng dùng Grok Bot; đây là cấp lượng dùng, không phải một gói Cursor [S17].
4. **Chỗ Grok Business.** Một chỗ được gán trong gói Grok Business tự phục vụ cấp lượng dùng như liên kết SuperGrok; chỉ một nguồn nêu điều này [S17].

Các đường này không cộng dồn: Grok Bot dùng đường nào cấp nhiều lượng dùng hằng tuần hơn [S17]. Lượng dùng lấy từ một bể hằng tuần chung với Cursor và các ứng dụng Grok, nên không có đồng hồ riêng cho Grok Bot [S17]. Hệ quả thực tế: người đã có một trong các gói trên có thể đã có quyền truy cập và không cần mua thêm; hãy kiểm tra gói đang có trước khi trả tiền (suy luận của người viết từ [S17]).

**Con số giá (nguồn thứ ba, có thể đã cũ).** Với chỗ ngồi nhóm của The X Subscription, tóm tắt tài liệu nêu $30, $100 và $200 mỗi chỗ cho Premium, Super và Ultra [S17]. Các bài tháng 8 và 9 mô tả theo tên gói trước đó: SuperGrok cơ bản khoảng $30, SuperGrok Plus khoảng $100, SuperGrok Heavy khoảng $300, Cursor Pro khoảng $20 [S9] [S11] [S12]. Một bài nói yêu cầu Heavy lúc ra mắt không còn đúng [S9]. Một bài nêu Cursor Ultra khoảng $200 và chưa có nguồn thứ hai xác nhận [S10]. Các con số này mâu thuẫn hoặc lệch tên gói với trang hiện hành, nên chỉ nên dùng để so sánh thô, không dùng để quyết định mua.

| Đường vào | Gói | Giá được nêu | Nguồn |
|---|---|---|---|
| The X Subscription | Premium, Super, Ultra | chỗ nhóm $30, $100, $200 | [S17] |
| Gói Cursor cũ | Pro, Pro+, Ultra, chỗ Teams | không nêu trong tài liệu; một bài so sánh ghi Pro khoảng $20 | [S12] [S17] |
| Liên kết tài khoản | SuperGrok, Plus, Heavy, X Premium+ | các bài cũ ghi khoảng $30, $100, $300 | [S11] [S17] |
| Chỗ Grok Business | chỗ được gán | không nêu | [S17] |

**Mâu thuẫn còn lại về danh sách gói.** Một bài tổng hợp ghi trang FAQ của xAI vẫn liệt kê tập gói hẹp hơn, bắt đầu từ Cursor Pro+ [S11]. Trang gói của Cursor liệt kê rộng hơn [S17]. Suy luận của người viết: nếu hai trang lệch nhau, theo trang ghi ngày mới hơn và mở trang giá chính thức vào đúng ngày mua.

**Dùng thử và hạn mức (nguồn chính thức và nguồn thứ ba).** Cursor mô tả dùng thử là một khoản tín dụng sử dụng trong cửa sổ bảy ngày; phần đã dùng không được hoàn lại, và một tác vụ lớn có thể dùng hết [S6]. Một nguồn khác ghi bảy ngày và phải nhập thẻ trước [S10]; nguồn khác ghi mười bốn ngày [S11]. Các gói trả phí có hạn mức hằng tuần, lấy từ một bể chung với Cursor và các ứng dụng Grok, mức cụ thể không được công bố, và không có trần chi riêng cho Grok Bot [S1] [S11] [S17]. Giới hạn chi tiêu đặt ở cấp tài khoản: với gói Cursor cũ là On-demand monthly limit trong Settings > Usage & Billing; với gói The X Subscription là bật Auto Top-up và đặt giới hạn dùng thêm hằng tháng ở trang thanh toán của grok.com, hoặc tắt Auto Top-up [S6]. Cursor lưu ý đây không phải ngưỡng cứng: một tác vụ đang chạy có thể vượt trần một chút [S6]. Người định dùng quá hạn mức hằng tuần nên đặt giới hạn này trước khi chạy nhiều Bot liên tục.

**Bản doanh nghiệp.** Một bài chụp trang giá ngày 10/09/2026 ghi Grok Bot chưa nằm trong gói Business hay Enterprise [S9]. Cursor ghi Team Setup chỉ dành cho Enterprise [S5].

## Ưu điểm

**Làm việc nền, không cần laptop (nguồn thứ ba).** Đây là điểm khác biệt nhất: việc theo lịch chạy tiếp khi bạn tắt máy [S8] [S9].

**Hành động trên công cụ thật (nguồn thứ ba).** Có trình duyệt, file và terminal nên Bot làm được việc như kiểm tra trang web, điền biểu mẫu, chạy lệnh, tạo file, chứ không chỉ trả lời văn bản [S8].

**Song song và phối hợp (nguồn chính thức).** Hai đến sáu Bot trong một nhóm, cùng nhận một đầu việc và chuyển việc cho nhau [S2].

**Có cổng kiểm soát cấu hình được (nguồn chính thức).** Allow once, Deny, Always allow, Auto Review và luật Ask first cho phép giữ con người trong vòng lặp với việc nhạy cảm, và tự động với việc lặp lại an toàn, nhưng đây là một lớp kiểm soát phải cấu hình, không phải bảo đảm (xem mục Giao việc) [S3] [S16] [S18].

**Cô lập giữa người dùng (nguồn chính thức).** Mỗi người một microVM với nhân riêng; người này không với tới máy của người kia [S5].

**Kết nối rộng (nguồn thứ ba).** Teams, Salesforce, SharePoint, chợ connector và MCP giúp Bot nối vào công cụ có sẵn của tổ chức [S2] [S8] [S14].

## Nhược điểm và rủi ro bảo mật

**Mọi Bot của một người dùng chung một máy (nguồn chính thức).** Cursor khuyến cáo coi mọi đăng nhập và file trên máy là có thể dùng được bởi mọi Bot của người đó; màn hình của từng Bot không phải ranh giới bảo mật [S4] [S5]. Vellum cũng chỉ ra rằng các Bot có thể truy cập cùng một phiên trình duyệt đã đăng nhập [S16]. Cách giảm thiểu được khuyến nghị: quyền tối thiểu, giao thông tin đăng nhập thủ công, luật Ask first hẹp và thu hồi quyền ở phía nguồn [S5] [S16].

**Phê duyệt chưa phải ranh giới bảo mật đã được chứng minh (nguồn chính thức).** Auto Review là một mô hình kiểm tra, không xem xét mọi tác dụng phụ, và chỉ luật Ask first mới luôn dừng hành động khớp luật; khóa Auto Review cho cả nhóm chỉ có ở Enterprise [S18]. Cấu hình lỏng hoặc quyền ghi rộng khiến Bot có thể làm việc có tác dụng phụ mà không xin phép [S1] [S18].

**Phiên đăng nhập có thể rơi (nguồn chính thức).** Máy đám mây được tạo lại sau cập nhật image hoặc đổi chính sách, và các phiên bên trong mất theo [S5].

**Chỉ trên hạ tầng Cursor, thiếu công cụ quản trị (nguồn chính thức).** Chưa có on-premises hay image tự mang; không có sẵn nguồn dữ liệu EDR cho khách hàng; Team Setup chỉ ở Enterprise [S5]. Một hướng dẫn nói thiếu màn hình kiểm toán đầy đủ mọi hành động của Bot [S16].

**Còn beta, giá và nền tảng đổi liên tục (nguồn thứ ba).** Gói được dùng đã đổi trong hai tuần đầu; nền tảng cũng bị mô tả khác nhau, một nguồn nói bản đầu chỉ có trên macOS Apple Silicon, tiêu đề Gigazine nêu cả Windows, macOS, Linux và iOS [S7] [S10].

**Thao tác trên trang đã đăng nhập chưa trơn tru (nguồn thứ ba, một thử nghiệm).** Mem0 thấy tác vụ trình duyệt trên trang công khai chạy được, còn chụp màn hình trang cần đăng nhập có thể đòi đăng nhập thêm [S8].

**Khó dự đoán chi phí sử dụng (nguồn chính thức).** Hạn mức hằng tuần không công bố và một tác vụ lớn có thể dùng hết khoản dùng thử [S6]. Suy luận của người viết: chạy nhiều Bot liên tục khó ước chi phí trước.

**Không chọn được mô hình, và nhà xử lý dữ liệu có thể là bên thứ ba (nguồn chính thức).** Không có bộ chọn mô hình; mỗi tác vụ dùng mô hình của xAI hoặc của nhà cung cấp bên thứ ba trong danh sách nhà xử lý phụ, và Cursor ghi allowlist của nhóm không chi phối Grok Bot [S15].

## Hệ sinh thái

**xAI (SpaceXAI) và dòng mô hình Grok.** Bên làm sản phẩm; Gigazine gọi bên phát hành là SpaceXAI [S7]. Tài liệu chính thức nằm ở docs.x.ai, gồm FAQ, chat và cộng tác, bảo mật [S1] [S2] [S3].

**Cursor.** Bên lưu trữ máy đám mây và có tài liệu riêng (bắt đầu, bảo mật, trợ giúp); Cursor Pro và Cursor Teams là hai đường vào [S4] [S5] [S6].

**The X Subscription và SuperGrok.** Đường mua trực tiếp từ xAI; The X Subscription có các bậc Premium, Super, Ultra gồm Grok Bot, còn tài khoản SuperGrok cá nhân có thể liên kết với tài khoản Cursor cũ [S17].

**Ứng dụng.** Ứng dụng iOS để duyệt và xem kết quả khi vắng bàn; một nguồn mô tả bản đầu trên macOS, nguồn khác thêm Windows [S7] [S10] [S14].

**Connector và routine.** Teams, Salesforce, SharePoint, danh mục bên thứ ba, chợ connector, MCP; email alias kích hoạt routine [S2] [S8] [S13] [S14].

**Hệ phụ trợ bên thứ ba.** Mem0, Vellum, Alarcon, Toolradar và nhiều blog viết hướng dẫn và đánh giá [S8] [S9] [S12] [S16]. Đây là phân tích, không phải tài liệu chính thức; nên đối chiếu khi một chi tiết quan trọng.

## Use case thực tế

**Khung chọn việc (nguồn thứ ba).** Alarcon đặt ba phép thử: việc lặp lại theo lịch; chạy được mà không cần file trên laptop; kết quả để lại cho bạn kiểm tra sau. Trượt một phép thử thì đó không phải việc của Bot [S9].

**Việc được nêu trong các bài đánh giá (nguồn thứ ba).** Mem0 liệt kê: theo dõi đối thủ cạnh tranh, kiểm tra kho mã, nghiên cứu nhiều nguồn song song, sinh mã, xác minh dữ kiện, lập kịch bản [S8].

**Áp dụng khung cho ba tình huống (suy luận của người viết, không phải kết quả đã kiểm).**

1. Mỗi sáng tóm tắt thay đổi trang giá và changelog của ba đối thủ: lặp lại, không cần file cục bộ, đọc kết quả sau. Đạt cả ba phép thử [S9].
2. Mỗi tuần quét repository để tìm dependency lỗi thời và issue cũ rồi tóm tắt: lặp lại, phụ thuộc kho trên đám mây. Đạt, nếu cấp quyền chỉ đọc [S8] [S5].
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

**Trước khi mua, kiểm tra** gói bạn đang có (Cursor, SuperGrok, X Premium, chỗ Grok Business) đã gồm Grok Bot chưa [S17].

**Nên thử khi** bạn có việc theo lịch cần chạy khi máy đã tắt; chấp nhận rằng mọi đăng nhập trên máy đám mây là chung cho các Bot của mình; bắt đầu bằng tài khoản và dữ liệu không nhạy cảm [S5] [S9].

**Chưa nên khi** bạn cần cách ly bảo mật giữa các tác vụ; cần triển khai trong hạ tầng riêng hoặc yêu cầu tuân thủ chặt; hoặc cần chi phí ổn định và dự đoán được [S5] [S6].

**Quy trình thử gợi ý (suy luận của người viết).** Chọn một việc đạt ba phép thử của Alarcon; chỉ cấp quyền tối thiểu; đặt luật Ask first cho mọi hành động ra ngoài như gửi thư, mua hàng, xóa (không dựa riêng vào Auto Review); xem bản ghi sau vài lần chạy rồi mới mở rộng; thu hồi quyền ở phía nguồn khi ngừng dùng [S5] [S9] [S18].

## Điều cần nhớ

Bốn ý. Một: Grok Bot là agent chạy nền trên máy tính đám mây, mạnh ở việc lặp lại theo lịch [S8] [S9]. Hai: các Bot của một người dùng chung một máy, nên đừng coi đó là cách ly [S5]. Ba: giá và gói truy cập chưa ổn định và các nguồn lệch nhau, hãy kiểm trang giá hiện hành [S11]. Bốn: đặt luật Ask first cho hành động ra ngoài và cấp quyền tối thiểu, vì phê duyệt là lớp bảo vệ cấu hình được chứ không phải bảo đảm [S3] [S18].

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
- [S15] Cursor, Which AI models power Grok Bot? (trợ giúp), 2026, https://cursor.com/help/grok-bot/models
- [S16] Vellum, Official Grok Bot breakdown, 2026, https://www.vellum.ai/blog/official-grok-bot-breakdown
- [S17] Cursor, Plans and billing (Grok Bot, trợ giúp), 2026, https://cursor.com/help/grok-bot/plans
- [S18] Cursor, Grok Bot security (tài liệu), 2026, https://cursor.com/docs/grok-bot/security
