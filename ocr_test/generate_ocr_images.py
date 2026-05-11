"""
OCR test image generator — English, Chinese, Korean, Japanese
Produces 400 PNG images (100 per language) with clear text and varied backgrounds.
Requirements: pip install pillow
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = "ocr_test_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Sample texts — 100 unique entries per language
# ---------------------------------------------------------------------------
TEXTS = {
    "english": [
        # Pangrams & classics
        "The quick brown fox jumps over the lazy dog.",
        "Pack my box with five dozen liquor jugs.",
        "How vexingly quick daft zebras jump!",
        "The five boxing wizards jump quickly.",
        "Sphinx of black quartz, judge my vow.",
        "Bright vixens jump; dozy fowl quack.",
        "Waltz, bad nymph, for quick jigs vex.",
        "Glib jocks quiz nymph to vex dwarf.",
        "Jackdaws love my big sphinx of quartz.",
        "The jay, pig, fox, zebra and my wolves quack.",
        # Sentences
        "She sells seashells by the seashore.",
        "Peter Piper picked a peck of pickled peppers.",
        "How much wood would a woodchuck chuck?",
        "To be or not to be, that is the question.",
        "All that glitters is not gold.",
        "The sun rises in the east and sets in the west.",
        "Reading and writing are fundamental skills.",
        "Optical Character Recognition works best with clear fonts.",
        "Machine learning models require quality training data.",
        "Knowledge is power. Information is liberating.",
        "A journey of a thousand miles begins with a single step.",
        "Time flies like an arrow; fruit flies like a banana.",
        "42 is the answer to life, the universe and everything.",
        "In the beginning was the Word, and the Word was with God.",
        "It was the best of times, it was the worst of times.",
        "Call me Ishmael.",
        "It is a truth universally acknowledged.",
        "Two roads diverged in a yellow wood.",
        "Do not go gentle into that good night.",
        "I have a dream that one day this nation will rise up.",
        # Alphanumeric / symbols
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "abcdefghijklmnopqrstuvwxyz",
        "0123456789",
        "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|`~",
        "The price is $19.99 (discounted from $29.99).",
        "Invoice #INV-2026-0042 | Amount: $1,234.56",
        "Email: support@example.com | Tel: +1-800-555-0199",
        "Address: 123 Main St, Springfield, NY 10001, USA",
        "Serial: XK-7749-ALPHA | Batch: 2026-Q2 | Qty: 500",
        "PIN: 8421 | Code: A7-BX-3Q | Ref: OCR-TEST-EN",
        # Mixed case / camel / acronyms
        "CamelCaseIdentifier and snake_case_variable",
        "HTTP/2.0 GET /api/v3/users?limit=50&offset=0",
        "SHA-256: e3b0c44298fc1c149afbf4c8996fb924",
        "UUID: 550e8400-e29b-41d4-a716-446655440000",
        "Base64: SGVsbG8gV29ybGQh",
        # Longer passages
        "The ability to read text from images has transformed document processing workflows.",
        "Neural networks have dramatically improved OCR accuracy over traditional methods.",
        "Modern OCR systems can handle multiple languages and scripts simultaneously.",
        "Training data quality directly impacts the performance of recognition models.",
        "Preprocessing steps like binarization and deskewing improve OCR results.",
        "Font variation is an important factor in building robust OCR test suites.",
        "Background noise and uneven lighting are common challenges in real-world OCR.",
        "High-resolution scans produce better recognition rates than low-DPI images.",
        "Post-processing with language models can correct common OCR mistakes.",
        "Evaluation metrics for OCR include character error rate and word error rate.",
        # Short phrases
        "Hello, World!",
        "Good morning.",
        "Thank you very much.",
        "Please sign here.",
        "Confidential document.",
        "Page 1 of 10",
        "Draft — Not for distribution",
        "Approved by: J. Smith",
        "Date: 2026-05-11",
        "Version: 3.1.4",
        # Numbers and codes
        "Latitude: 40.7128° N, Longitude: 74.0060° W",
        "Temperature: 23.5°C | Humidity: 65% | Pressure: 1013 hPa",
        "RGB(255, 128, 0) | HEX #FF8000 | HSL(30°, 100%, 50%)",
        "2026-05-11T14:30:00Z (ISO 8601)",
        "Barcode: 978-0-306-40615-7",
        "Part No. 4821-C | Weight: 2.75 kg | Dims: 30×20×15 cm",
        "Score: 98/100 | Grade: A+ | Rank: 1st",
        "Speed: 120 km/h | Distance: 350 km | ETA: 14:30",
        "Voltage: 220V AC 50Hz | Current: 10A | Power: 2200W",
        "pH 7.4 | Concentration: 0.9% NaCl | Volume: 500 mL",
        # Real-world document snippets
        "TERMS AND CONDITIONS — Please read carefully before use.",
        "WARRANTY: This product is warranted against defects for 12 months.",
        "CAUTION: Keep out of reach of children under 3 years old.",
        "IMPORTANT NOTICE: Service will be interrupted from 02:00–04:00 UTC.",
        "CHAPTER 1: Introduction to Optical Character Recognition",
        "Section 3.2: Data Preprocessing and Augmentation Techniques",
        "Figure 4: Comparison of CER across different model architectures.",
        "Table 1: Benchmark results on standard OCR datasets.",
        "Appendix A: Font samples used in training data generation.",
        "References: [1] LeCun et al. (1998) [2] Goodfellow et al. (2016)",
        # Mixed content
        "Wi-Fi Password: MyS3cur3P@ssw0rd!",
        "Meeting Room B | Capacity: 20 | Floor: 3 | Ext: 4201",
        "Flight QR-742 | Gate B12 | Boarding: 13:45 | Seat: 24A",
        "Order #ORD-88421 | Status: Shipped | Track: 1Z999AA10123456784",
        "Patient ID: PT-20260511 | DOB: 1985-03-22 | Blood: O+",
        "Vehicle: Toyota Camry 2024 | Plate: ABC-1234 | VIN: 1HGBH41JXMN109186",
        "Recipe: Mix 250g flour, 2 eggs, 150ml milk. Bake 180°C for 25 min.",
        "Formula: E = mc² | F = ma | PV = nRT | λ = h/p",
        "Hex dump: 48 65 6C 6C 6F 20 57 6F 72 6C 64",
        "Network: 192.168.1.0/24 | Gateway: 192.168.1.1 | DNS: 8.8.8.8",
    ],
    "chinese": [
        # 日常句子
        "快速的棕色狐狸跳过了懒狗。",
        "光学字符识别是人工智能的重要组成部分。",
        "中文文字识别需要高质量的训练数据。",
        "今天天气很好，阳光明媚，微风习习。",
        "人工智能技术正在快速改变我们的生活。",
        "北京是中国的首都，拥有悠久的历史文化。",
        "上海是中国最大的经济和金融中心。",
        "中华人民共和国成立于一九四九年十月一日。",
        "科学技术是第一生产力，创新是发展的驱动力。",
        "机器学习模型需要大量高质量的标注数据。",
        # 古诗词
        "学而不思则罔，思而不学则殆。",
        "千里之行，始于足下。",
        "知识就是力量，信息就是解放。",
        "人无远虑，必有近忧。",
        "春眠不觉晓，处处闻啼鸟。",
        "床前明月光，疑是地上霜。",
        "举头望明月，低头思故乡。",
        "海内存知己，天涯若比邻。",
        "山重水复疑无路，柳暗花明又一村。",
        "会当凌绝顶，一览众山小。",
        "落霞与孤鹜齐飞，秋水共长天一色。",
        "君不见黄河之水天上来，奔流到海不复回。",
        "但使龙城飞将在，不教胡马度阴山。",
        "欲穷千里目，更上一层楼。",
        "天生我材必有用，千金散尽还复来。",
        # 数字与符号
        "数字：零一二三四五六七八九十",
        "汉字数字：壹贰叁肆伍陆柒捌玖拾",
        "符号：，。！？；：""''（）【】《》",
        "订单编号：2026-05-0042 总金额：¥1,234.56",
        "联系电话：010-8888-9999 邮编：100000",
        "地址：北京市朝阳区建国路88号国贸大厦A座",
        "产品型号：XK-7749 批次：2026年第二季度",
        "身份证号：110101199003072518",
        "银行卡号：6222 0000 1234 5678",
        "统一社会信用代码：91110000100000001X",
        # 技术文档
        "神经网络已经显著提高了OCR的识别准确率。",
        "预处理步骤如二值化和去倾斜能改善OCR结果。",
        "背景噪声和不均匀光照是实际OCR中的常见挑战。",
        "字体变化是构建健壮OCR测试套件的重要因素。",
        "高分辨率扫描比低DPI图像产生更好的识别率。",
        "现代OCR系统可以同时处理多种语言和文字。",
        "后处理语言模型可以纠正常见的OCR错误。",
        "训练数据质量直接影响识别模型的性能表现。",
        "字符错误率和词错误率是OCR的常用评估指标。",
        "数据增强技术可以有效扩充训练数据集的规模。",
        # 生活场景
        "请输入您的用户名和密码以登录系统。",
        "系统检测到异常登录，请立即修改密码。",
        "数据处理完成，共处理记录10,000条，成功率99.8%。",
        "欢迎使用智能文字识别系统，请选择识别语言。",
        "您的快递已签收，感谢您使用我们的服务。",
        "会议将于明天上午九点在三楼会议室举行。",
        "请在规定时间内完成表格填写并提交审核。",
        "系统将于今晚22:00进行例行维护，预计持续2小时。",
        "您的订单已发货，预计3-5个工作日内送达。",
        "感谢您的反馈，我们将持续改进产品和服务。",
        # 专业术语
        "人工智能、机器学习、深度学习、自然语言处理。",
        "卷积神经网络在图像识别领域取得了突破性进展。",
        "循环神经网络适合处理序列数据和时间序列。",
        "注意力机制是Transformer模型的核心组件。",
        "迁移学习可以利用预训练模型加速新任务的学习。",
        "数据标注是监督学习中最耗时耗力的环节之一。",
        "模型压缩和量化技术用于在边缘设备上部署AI。",
        "联邦学习在保护隐私的同时实现分布式模型训练。",
        "强化学习通过试错机制让智能体学习最优策略。",
        "生成对抗网络可以生成以假乱真的图像和文本。",
        # 混合内容
        "产品规格：长30cm×宽20cm×高15cm，重量2.75kg",
        "温度：23.5°C | 湿度：65% | 气压：1013 hPa",
        "坐标：北纬40.7128°，东经116.4074°",
        "化学式：H₂O、CO₂、NaCl、C₆H₁₂O₆",
        "数学公式：E=mc²，F=ma，PV=nRT",
        "航班：CA-742 | 登机口：B12 | 登机时间：13:45",
        "患者编号：PT-20260511 | 血型：O型 | 年龄：41岁",
        "食谱：将250克面粉、2个鸡蛋、150毫升牛奶混合均匀。",
        "网络：192.168.1.0/24 | 网关：192.168.1.1",
        "条形码：978-7-5321-1234-5 | 定价：¥88.00",
        # 短语
        "你好！",
        "早上好。",
        "非常感谢。",
        "请在此签字。",
        "机密文件。",
        "第1页，共10页",
        "草稿——请勿外传",
        "审批人：张三",
        "日期：2026年5月11日",
        "版本：3.1.4",
        # 新闻标题风格
        "全球气候变化峰会在巴黎召开，各国领导人共商对策。",
        "新型人工智能芯片发布，计算性能提升十倍。",
        "科学家发现新型抗癌药物，临床试验效果显著。",
        "国际空间站迎来新一批宇航员，将开展多项科学实验。",
        "全球经济论坛年会开幕，数字经济成为重点议题。",
    ],
    "korean": [
        # 일상 문장
        "빠른 갈색 여우가 게으른 개를 뛰어넘습니다.",
        "광학 문자 인식은 인공지능의 중요한 부분입니다.",
        "한국어 문자 인식을 위한 테스트 이미지입니다.",
        "안녕하세요! 오늘도 좋은 하루 되세요.",
        "서울은 대한민국의 수도이자 최대 도시입니다.",
        "기계 학습 모델은 고품질 데이터가 필요합니다.",
        "인공지능 기술이 빠르게 발전하고 있습니다.",
        "대한민국은 아시아 동부 한반도에 위치해 있습니다.",
        "세종대왕은 훈민정음(한글)을 창제하셨습니다.",
        "과학 기술이 우리 생활을 크게 변화시키고 있습니다.",
        # 자음과 모음
        "가나다라마바사아자차카타파하",
        "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ",
        "ㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣ",
        "가각간갈감갑강개객거건걸검겁게격견결겸경",
        "숫자: 일이삼사오육칠팔구십백천만억",
        # 속담과 격언
        "아는 것이 힘이다.",
        "시작이 반이다.",
        "천 리 길도 한 걸음부터.",
        "배움에는 끝이 없다.",
        "하늘은 스스로 돕는 자를 돕는다.",
        "가는 말이 고와야 오는 말이 곱다.",
        "낮말은 새가 듣고 밤말은 쥐가 듣는다.",
        "세 살 버릇 여든까지 간다.",
        "원숭이도 나무에서 떨어진다.",
        "호랑이에게 물려가도 정신만 차리면 산다.",
        # 숫자와 기호
        "주문번호: 2026-05-0042 금액: ₩1,234,560",
        "연락처: 02-1234-5678 우편번호: 04524",
        "주소: 서울특별시 강남구 테헤란로 123번길 45",
        "모델번호: XK-7749 배치: 2026년 2분기",
        "주민등록번호: 850322-1234567 (예시용)",
        "사업자등록번호: 123-45-67890",
        "계좌번호: 012-345678-01-001 (국민은행)",
        "차량번호: 12가 3456 | 차종: 현대 소나타",
        "온도: 23.5°C | 습도: 65% | 기압: 1013 hPa",
        "좌표: 북위 37.5665°, 동경 126.9780°",
        # 기술 문서
        "신경망은 OCR 인식 정확도를 크게 향상시켰습니다.",
        "이진화 및 기울기 보정 등의 전처리로 OCR 결과를 개선할 수 있습니다.",
        "배경 노이즈와 불균일한 조명은 실제 OCR의 일반적인 과제입니다.",
        "글꼴 다양성은 강력한 OCR 테스트 스위트 구축의 중요한 요소입니다.",
        "고해상도 스캔은 저DPI 이미지보다 더 나은 인식률을 제공합니다.",
        "현대 OCR 시스템은 여러 언어와 문자를 동시에 처리할 수 있습니다.",
        "언어 모델을 이용한 후처리로 일반적인 OCR 오류를 교정할 수 있습니다.",
        "훈련 데이터 품질은 인식 모델의 성능에 직접적인 영향을 미칩니다.",
        "문자 오류율과 단어 오류율은 OCR의 일반적인 평가 지표입니다.",
        "데이터 증강 기술은 훈련 데이터셋의 규모를 효과적으로 확장합니다.",
        # 생활 장면
        "사용자 이름과 비밀번호를 입력해 주세요.",
        "시스템 오류가 감지되었습니다. 관리자에게 문의하세요.",
        "데이터 처리 완료. 총 10,000개의 레코드 처리됨 (성공률 99.8%).",
        "스마트 문자 인식 시스템에 오신 것을 환영합니다!",
        "택배가 도착했습니다. 이용해 주셔서 감사합니다.",
        "회의는 내일 오전 9시 3층 회의실에서 열립니다.",
        "정해진 시간 내에 양식을 작성하고 제출해 주세요.",
        "시스템은 오늘 밤 22:00에 정기 점검이 있을 예정입니다.",
        "주문이 발송되었습니다. 3~5 영업일 내 도착 예정입니다.",
        "귀하의 소중한 의견 감사합니다. 더욱 발전하겠습니다.",
        # 전문 용어
        "인공지능, 기계 학습, 딥러닝, 자연어 처리",
        "합성곱 신경망은 이미지 인식 분야에서 획기적인 성과를 거뒀습니다.",
        "순환 신경망은 순차 데이터와 시계열 처리에 적합합니다.",
        "어텐션 메커니즘은 트랜스포머 모델의 핵심 구성 요소입니다.",
        "전이 학습은 사전 훈련된 모델을 활용해 새 작업 학습을 가속합니다.",
        "데이터 레이블링은 지도 학습에서 가장 시간이 많이 걸리는 단계입니다.",
        "모델 압축 및 양자화 기술은 엣지 장치에서 AI를 배포하는 데 사용됩니다.",
        "연합 학습은 개인정보를 보호하면서 분산 모델 학습을 실현합니다.",
        "강화 학습은 시행착오를 통해 에이전트가 최적 전략을 배우게 합니다.",
        "생성적 적대 신경망은 사실적인 이미지와 텍스트를 생성할 수 있습니다.",
        # 뉴스 헤드라인 스타일
        "글로벌 기후 변화 정상회담, 파리에서 개최.",
        "새로운 AI 칩 출시, 연산 성능 10배 향상.",
        "과학자들, 새로운 항암제 발견—임상시험 결과 유망.",
        "국제 우주 정거장에 새 우주인 합류, 다양한 실험 예정.",
        "세계 경제 포럼 연차 총회 개막, 디지털 경제 집중 논의.",
        # 짧은 문구
        "안녕!",
        "좋은 아침입니다.",
        "대단히 감사합니다.",
        "여기에 서명해 주세요.",
        "기밀 문서.",
        "1페이지 / 총 10페이지",
        "초안 — 배포 금지",
        "승인자: 홍길동",
        "날짜: 2026년 5월 11일",
        "버전: 3.1.4",
    ],
    "japanese": [
        # 日常の文章
        "素早い茶色のキツネが怠け者の犬を飛び越えます。",
        "光学文字認識は人工知能の重要な要素です。",
        "日本語のテキスト認識テスト用画像です。",
        "こんにちは！今日もよい一日をお過ごしください。",
        "東京は日本の首都であり、最大の都市です。",
        "機械学習モデルには高品質なデータが必要です。",
        "人工知能技術は急速に発展しています。",
        "日本は太平洋に位置する東アジアの島国です。",
        "科学技術は私たちの生活を大きく変えています。",
        "データの品質が認識モデルの性能に直結します。",
        # 平仮名・片仮名
        "あいうえおかきくけこさしすせそたちつてとなにぬねの",
        "はひふへほまみむめもやゆよらりるれろわをん",
        "アイウエオカキクケコサシスセソタチツテトナニヌネノ",
        "ハヒフヘホマミムメモヤユヨラリルレロワヲン",
        "一二三四五六七八九十百千万億兆",
        # ことわざ・格言
        "知識は力なり。",
        "始まりは半ば。",
        "千里の道も一歩から。",
        "学ぶことに終わりはない。",
        "七転び八起き。",
        "失敗は成功の母。",
        "継続は力なり。",
        "急がば回れ。",
        "石の上にも三年。",
        "論より証拠。",
        # 漢詩・古典
        "春はあけぼの。やうやう白くなりゆく山際。",
        "祇園精舎の鐘の声、諸行無常の響きあり。",
        "行く川のながれは絶えずして、しかも本の水にあらず。",
        "吾輩は猫である。名前はまだ無い。",
        "国境の長いトンネルを抜けると雪国であった。",
        # 数字・記号
        "注文番号: 2026-05-0042 金額: ¥123,456",
        "電話番号: 03-1234-5678 郵便番号: 100-0001",
        "住所: 東京都千代田区丸の内1丁目1番地",
        "型番: XK-7749 バッチ: 2026年第2四半期",
        "マイナンバー: 1234-5678-9012 (例示用)",
        "口座番号: 1234-567890 (三菱UFJ銀行)",
        "車両番号: 品川 300 あ 1234",
        "気温: 23.5°C | 湿度: 65% | 気圧: 1013 hPa",
        "座標: 北緯35.6762°, 東経139.6503°",
        "バーコード: 978-4-10-109061-8 | 定価: ¥1,650",
        # 技術文書
        "ニューラルネットワークはOCR認識精度を大幅に向上させました。",
        "二値化や傾き補正などの前処理でOCR結果を改善できます。",
        "背景ノイズや不均一な照明は実世界OCRの一般的な課題です。",
        "フォントの多様性は堅牢なOCRテストスイート構築の重要な要素です。",
        "高解像度スキャンは低DPI画像より優れた認識率を提供します。",
        "現代のOCRシステムは複数の言語と文字を同時に処理できます。",
        "言語モデルを使った後処理で一般的なOCRエラーを修正できます。",
        "訓練データの品質は認識モデルのパフォーマンスに直接影響します。",
        "文字誤り率と単語誤り率はOCRの一般的な評価指標です。",
        "データ拡張技術は訓練データセットの規模を効果的に拡大します。",
        # 生活シーン
        "ユーザー名とパスワードを入力してください。",
        "システムエラーが検出されました。管理者にお問い合わせください。",
        "データ処理完了。合計10,000件のレコードを処理しました（成功率99.8%）。",
        "スマート文字認識システムへようこそ！",
        "お荷物が届きました。ご利用ありがとうございます。",
        "会議は明日の午前9時、3階の会議室で行われます。",
        "所定の時間内にフォームに記入して提出してください。",
        "システムは本日22:00から定期メンテナンスを行います。",
        "ご注文が発送されました。3〜5営業日以内にお届け予定です。",
        "貴重なご意見をいただきありがとうございます。",
        # 専門用語
        "人工知能、機械学習、深層学習、自然言語処理",
        "畳み込みニューラルネットワークは画像認識で革新的な成果を上げました。",
        "再帰型ニューラルネットワークは系列データや時系列の処理に適しています。",
        "アテンション機構はTransformerモデルの核心コンポーネントです。",
        "転移学習は事前学習済みモデルを活用して新タスクの学習を加速します。",
        "データラベリングは教師あり学習で最も時間のかかる工程の一つです。",
        "モデル圧縮と量子化技術はエッジデバイスへのAI展開に使われます。",
        "連合学習はプライバシーを保護しながら分散モデル訓練を実現します。",
        "強化学習は試行錯誤を通じてエージェントが最適戦略を学びます。",
        "生成的敵対ネットワークはリアルな画像やテキストを生成できます。",
        # ニュース見出し風
        "地球温暖化サミット、パリで開幕。各国首脳が対策を協議。",
        "新型AIチップ発売。演算性能が10倍に向上。",
        "科学者が新たな抗がん剤を発見。臨床試験で顕著な効果。",
        "国際宇宙ステーションに新クルー到着。多数の実験を予定。",
        "世界経済フォーラム年次総会開幕。デジタル経済が焦点に。",
        # 短いフレーズ
        "こんにちは！",
        "おはようございます。",
        "ありがとうございます。",
        "こちらにご署名ください。",
        "機密文書。",
        "1ページ目 / 全10ページ",
        "下書き — 配布禁止",
        "承認者：田中太郎",
        "日付：2026年5月11日",
        "バージョン：3.1.4",
    ],
}

# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
FONTS = {
    "english": [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
        r"C:\Windows\Fonts\calibrib.ttf",
        r"C:\Windows\Fonts\times.ttf",
        r"C:\Windows\Fonts\timesbd.ttf",
        r"C:\Windows\Fonts\cour.ttf",
        r"C:\Windows\Fonts\georgia.ttf",
        r"C:\Windows\Fonts\verdana.ttf",
        r"C:\Windows\Fonts\tahoma.ttf",
    ],
    "chinese": [
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\msyhbd.ttc",
        r"C:\Windows\Fonts\simsun.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\STKAITI.TTF",
        r"C:\Windows\Fonts\STFANGSO.TTF",
    ],
    "korean": [
        r"C:\Windows\Fonts\malgun.ttf",
        r"C:\Windows\Fonts\malgunbd.ttf",
        r"C:\Windows\Fonts\gulim.ttc",
        r"C:\Windows\Fonts\batang.ttc",
    ],
    "japanese": [
        r"C:\Windows\Fonts\meiryo.ttc",
        r"C:\Windows\Fonts\meiryob.ttc",
        r"C:\Windows\Fonts\yugothm.ttc",
        r"C:\Windows\Fonts\yugothb.ttc",
        r"C:\Windows\Fonts\YuMincho.ttc",
    ],
}

# ---------------------------------------------------------------------------
# Image settings
# ---------------------------------------------------------------------------
IMAGE_SIZES = [
    (800, 200), (1000, 140), (640, 180), (900, 260),
    (720, 200), (1100, 160), (850, 220), (600, 160),
]
FONT_SIZES = [28, 32, 36, 40, 44, 48]

# Dark-text colors (used on light backgrounds)
DARK_TEXT = [
    (0,   0,   0),
    (20,  20,  80),
    (60,  0,   0),
    (0,   60,  0),
    (30,  30,  30),
    (50,  0,   50),
    (0,   50,  50),
    (80,  40,  0),
]

# Light-text colors (used on dark backgrounds)
LIGHT_TEXT = [
    (255, 255, 255),
    (220, 220, 255),
    (255, 220, 220),
    (220, 255, 220),
    (255, 255, 180),
    (200, 240, 255),
]


# ---------------------------------------------------------------------------
# Background generators — 10 distinct styles
# ---------------------------------------------------------------------------

def bg_solid_light(size):
    palettes = [
        (255, 255, 255), (245, 245, 245), (250, 250, 240),
        (240, 248, 255), (245, 255, 245), (255, 248, 240),
        (255, 245, 255), (240, 255, 255),
    ]
    return Image.new("RGB", size, random.choice(palettes)), "dark"


def bg_solid_dark(size):
    palettes = [
        (20,  20,  20),  (0,   0,   60),  (60,  0,   0),
        (0,   60,  0),   (30,  0,   60),  (0,   40,  60),
        (50,  30,  0),   (40,  40,  40),
    ]
    return Image.new("RGB", size, random.choice(palettes)), "light"


def bg_solid_pastel(size):
    r = random.randint(180, 230)
    g = random.randint(180, 230)
    b = random.randint(180, 230)
    return Image.new("RGB", size, (r, g, b)), "dark"


def bg_gradient_horizontal(size):
    w, h = size
    c1 = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
    c2 = (random.randint(150, 210), random.randint(150, 210), random.randint(150, 210))
    img = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)
    for x in range(w):
        t = x / w
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        draw.line([(x, 0), (x, h)], fill=(r, g, b))
    return img, "dark"


def bg_gradient_vertical(size):
    w, h = size
    c1 = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
    c2 = (random.randint(140, 200), random.randint(140, 200), random.randint(140, 200))
    img = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return img, "dark"


def bg_gradient_dark(size):
    w, h = size
    c1 = (random.randint(0, 60), random.randint(0, 60), random.randint(0, 80))
    c2 = (random.randint(40, 100), random.randint(0, 60), random.randint(60, 120))
    img = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)
    for x in range(w):
        t = x / w
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        draw.line([(x, 0), (x, h)], fill=(r, g, b))
    return img, "light"


def bg_noise_light(size):
    img = Image.new("RGB", size, (245, 245, 245))
    pixels = img.load()
    for y in range(size[1]):
        for x in range(size[0]):
            n = random.randint(-12, 12)
            r, g, b = pixels[x, y]
            pixels[x, y] = (
                max(0, min(255, r + n)),
                max(0, min(255, g + n)),
                max(0, min(255, b + n)),
            )
    return img, "dark"


def bg_noise_dark(size):
    base = random.randint(20, 60)
    img = Image.new("RGB", size, (base, base, base + 10))
    pixels = img.load()
    for y in range(size[1]):
        for x in range(size[0]):
            n = random.randint(-15, 15)
            r, g, b = pixels[x, y]
            pixels[x, y] = (
                max(0, min(255, r + n)),
                max(0, min(255, g + n)),
                max(0, min(255, b + n)),
            )
    return img, "light"


def bg_grid_light(size):
    img = Image.new("RGB", size, (255, 255, 255))
    draw = ImageDraw.Draw(img)
    step = random.choice([20, 25, 30, 40])
    color = (210, 220, 235)
    for x in range(0, size[0], step):
        draw.line([(x, 0), (x, size[1])], fill=color, width=1)
    for y in range(0, size[1], step):
        draw.line([(0, y), (size[0], y)], fill=color, width=1)
    return img, "dark"


def bg_lined_paper(size):
    img = Image.new("RGB", size, (255, 253, 240))
    draw = ImageDraw.Draw(img)
    step = random.choice([28, 32, 36])
    for y in range(0, size[1], step):
        draw.line([(0, y), (size[0], y)], fill=(180, 200, 230), width=1)
    return img, "dark"


def bg_gradient_diagonal(size):
    w, h = size
    light = random.choice([True, False])
    if light:
        c1 = (random.randint(220, 255), random.randint(220, 255), random.randint(220, 255))
        c2 = (random.randint(160, 210), random.randint(160, 210), random.randint(160, 210))
        mode = "dark"
    else:
        c1 = (random.randint(0, 40), random.randint(0, 60), random.randint(40, 100))
        c2 = (random.randint(40, 100), random.randint(0, 50), random.randint(0, 60))
        mode = "light"
    img = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)
    for x in range(w):
        for y in range(h):
            t = (x / w + y / h) / 2
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            draw.point((x, y), fill=(r, g, b))
    return img, mode


def bg_blueprint(size):
    img = Image.new("RGB", size, (20, 50, 100))
    draw = ImageDraw.Draw(img)
    step = 20
    color = (40, 80, 140)
    for x in range(0, size[0], step):
        draw.line([(x, 0), (x, size[1])], fill=color, width=1)
    for y in range(0, size[1], step):
        draw.line([(0, y), (size[0], y)], fill=color, width=1)
    return img, "light"


def bg_aged_paper(size):
    r_base = random.randint(220, 240)
    g_base = random.randint(200, 220)
    b_base = random.randint(160, 185)
    img = Image.new("RGB", size, (r_base, g_base, b_base))
    pixels = img.load()
    for y in range(size[1]):
        for x in range(size[0]):
            n = random.randint(-10, 10)
            pv = pixels[x, y]
            pixels[x, y] = (
                max(0, min(255, pv[0] + n)),
                max(0, min(255, pv[1] + n)),
                max(0, min(255, pv[2] + n)),
            )
    return img, "dark"


def bg_colorful_solid(size):
    hue_r = random.randint(0, 255)
    hue_g = random.randint(0, 255)
    hue_b = random.randint(0, 255)
    brightness = (hue_r * 299 + hue_g * 587 + hue_b * 114) / 1000
    mode = "light" if brightness < 128 else "dark"
    return Image.new("RGB", size, (hue_r, hue_g, hue_b)), mode


BACKGROUND_STYLES = [
    bg_solid_light,
    bg_solid_dark,
    bg_solid_pastel,
    bg_gradient_horizontal,
    bg_gradient_vertical,
    bg_gradient_dark,
    bg_noise_light,
    bg_noise_dark,
    bg_grid_light,
    bg_lined_paper,
    bg_gradient_diagonal,
    bg_blueprint,
    bg_aged_paper,
    bg_colorful_solid,
]


def pick_font(lang, size):
    candidates = list(FONTS[lang])
    random.shuffle(candidates)
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def make_image(text, lang, index, total):
    size = random.choice(IMAGE_SIZES)
    font_size = random.choice(FONT_SIZES)

    bg_fn = BACKGROUND_STYLES[index % len(BACKGROUND_STYLES)]
    img, text_mode = bg_fn(size)
    draw = ImageDraw.Draw(img)
    font = pick_font(lang, font_size)

    text_color = random.choice(LIGHT_TEXT if text_mode == "light" else DARK_TEXT)

    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = max(10, (size[0] - tw) // 2)
    y = max(5,  (size[1] - th) // 2)

    # Subtle drop shadow
    shadow_color = (0, 0, 0, 80) if text_mode == "dark" else (200, 200, 200)
    draw.text((x + 1, y + 1), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=text_color)

    lang_dir = os.path.join(OUTPUT_DIR, lang)
    os.makedirs(lang_dir, exist_ok=True)
    filename = os.path.join(lang_dir, f"{index:03d}.png")
    img.save(filename, "PNG")
    return filename


def main():
    languages = ["english", "chinese", "korean", "japanese"]
    total_per_lang = 100
    grand_total = len(languages) * total_per_lang
    count = 0

    for lang in languages:
        texts = TEXTS[lang]
        print(f"\n--- {lang.upper()} ---")
        for i in range(total_per_lang):
            text  = texts[i % len(texts)]
            count += 1
            path  = make_image(text, lang, i + 1, grand_total)
            print(f"  [{count:3d}/{grand_total}] {path}")

    print(f"\nDone. {count} images saved under '{OUTPUT_DIR}/'")
    print(f"  {OUTPUT_DIR}/english/  001–100")
    print(f"  {OUTPUT_DIR}/chinese/  001–100")
    print(f"  {OUTPUT_DIR}/korean/   001–100")
    print(f"  {OUTPUT_DIR}/japanese/ 001–100")


if __name__ == "__main__":
    main()
