# Rate-AI
### PROJENİN HEDEFLERİ :
  - Proje, ürünlere ait yorumların yapay zeka desteği ile daha yüksek doğrulukta puanlanmasını amaçlar.
  - Çoğu üründe kullanıcıların yorumları ve puanları arasında tutarsızlıklar görülmektedir. Proje bu sorunu çözmeye odaklanıyor.

<p>&nbsp;</p>

### UYGULAMANIN SAĞLADIĞI ÖZELLİKLER :
  - Dosyaların yüklenip işlemler yapılması ve kullanıcın doğruluğu test etmesi aşamalarından oluşmaktadır.
    <p>&nbsp;</p>
  ### Beni Test Et :
    - Yeni kullanıcıların modelin doğruluğunu test etmesi amacıyla oluşturulmuştur.
    - Sonucunu görmek istediğiniz yorumu yüklediğinizde size 7 farklı değerlendirme sonucundan en uygun olanı döndürüyor.
    - Skala : 
      - kesinikle (olumlu/olumsuz)
      - (olumlu/olumsuz)
      - emin değilim ama (olumlu/olumsuz)
      - karar veremedim

<p>&nbsp;</p>
  
  ### Analiz Et :
    
    - Çok sayıda yorumu tek tek puanlamak yerine daha genel bir değerlendirme sunar.
    - Tüm yorumları detaylı bir şekilde analiz eder ve ortalama puanı yüzdelik değer olarak sunar.
    - Bu sayede ürüne ait ortalama puana kısa sürede erişilebiliyor.
    - Veritabanına, dosyanın konumu ve analiz sonucu kaydedilir.
    - Böylece analiz edilmiş her dosyaya ait sonuca tek bir sorguyla ulaşılabiliyor.

<p>&nbsp;</p>
  
  ### Puanla : 
  
    - Model yüklenen her yorum için 1-5 yıldız aralığında puan veriyor.
    - Puanlanmış yorumlar seçilen dosyanın olduğu konuma csv olarak kaydediliyor. 
    - Ayrıca uygulamanın kendi arayüzünden de puanlar görüntülenebilir.
  
  <p>&nbsp;</p> 
  
  NOT: Hem 'Analiz Et' hem de 'Puanla' bölümlerindeki kayıt sistemi sayesinde, daha önce işlem yaptığınız dosyayı tekrar yüklediğinizde program sonuçları otomatik olarak görüntüler.
  
  <p>&nbsp;</p>  


### VERİ SETİNİN HAZIRLANMASI :
  - Verileri requests ve bs4 modülleriyle kendim toplamayı denedim. Birçok majör websitesi Response[200] döndürmediği için 'denebunu.com' ve 'beyazperde.com' sitelerinden faydalandım.
  
  - Bu iki farklı websitesi için 2 farklı algoritma kullanmam gerekti.


    <p>&nbsp;</p>   

      ### Beyazperde :
    - Beyazperde sitesinde tüm filmler {film-1,film-1352,film-35264...} şeklinde etiketlenmiş. Ayrıca yorumlar ve ratinglere html parser ile ulaşılabiliyor. Bu sayede çok daha efektif bir kodla yorumları çekebildim. Kısaca özetlemek gerekirse:
   
      
      - Algoritma {film-1}den başlayarak tüm url'leri geziyor. Eğer film sayfasında herhangi bir yorum yoksa sayfayı atlıyor ve diğer filme ait sayfayı kontrol ediyor.
      - Eğer yorum bulabilirse 3 puan ve üstü yorumları (1) olumlu, 2 puan ve altı yorumları (0) olumsuz olarak etiketliyor. Ve her yeni film taramasına geçmeden önce bu yorumları etiketleriyle birlikte .csv uzantılı dosyaya kaydediyor.
      - Eşzamanlı olarak en son taranan filmin id'si sürekli olarak güncelleniyor. Böylece siz programı kapatıp tekrar başlattığınızda en baştan taramak yerine kaldığınız noktadan devam ediyor.
      - Ayıca her kaydedilen filmin id'si ve bulduğu yorum sayısını .db uzantılı dosyaya kaydediyor. Böylece dosyada olası bir bozulma durumu yaşanması halinde sıfırdan tarama yapmanız gerekse bile boş sayfaları tekrar tekrar gezmeniz gerekmeyecek.
      - Vizyondaki son filme ait id'nin 330.000 civarında olduğunu düşünürsek bu da ciddi bir maliyet kaybının önlenmesi demek.


    <p>&nbsp;</p> 

    ### Denebunu :
    - Kullanıcı ratinglerini htmlde direkt olarak paylaşmak yerine yalnızca fotoğraf koymayı tercih etmişler. Ve ürünlerin url'leri ürün ismiyle kaydedilmiş. Dolayısıyla beyazperde sitesindeki kadar otomatik bir yöntem kullanamadım. Ancak özetlemek gerekirse algoritmam şu şekilde çalışıyor:
   
      
      - Öncelikle ürüne ait yorumlar sayfalarını azalandan artana (1-5) şeklinde sıralanacak sayfadan aldım böylece yorumların sayfaları puanlarına göre ayrılmış oldu.
      - Olumsuz etiketlerin üst sınırı : 2 puanların bittiği ve 3 puanların başladığı sayfa olumsuz etiketlerin üst sınırı olarak belirleniyor.
      - Olumlu etiketlerin alt sınırı : Teorik olarak 3 puanların bittiği ve 4 puanların başladığı sayfanın da olumlu etiketlerin alt sınırı olarak belirlenmesi gerekirdi ancak daha dengeli bir veri seti elde edebilmek için belirli bir noktadan itibaren olumsuz yorum sayfa sayısı kadar alındı.
      - Örnek vermek gerekirse ürüne ait 1000 adet yorum sayfası olsun. Birinci sayfadan itibaren 1 yıldızlı ürünler sıralanıyor. Giderek de yıldız sayısı artıyor. 2 puanların bittiği sayfa 215 ve 3 puanların bittiği sayfa 643 ise fonksiyonu #get_comments_and_ratings(215,643,1000,"product_name") şeklinde çağırıyoruz.
      -  Böylece ilk 215 sayfadaki yorumlar (0) ve son 357 sayfadaki yorumlar (1) olarak etiketleniyor.
      -  Tıpkı beyazperdede olduğu gibi bu yorumlar da .csv dosyasına kaydediliyor, ürünün adı ve etiketlerin başlangıç-bitiş noktası bilgileri .db dosyasına kaydediliyor.



<p>&nbsp;</p> 

### Uygulamanın Geliştirilebilecek Yönleri :
   - Analiz edilen ürün türüne göre daha spesifik sonuçlar verilebilir.
   - Daha derinlemesine analiz yapabilen gelişmiş modellerden faydalanılabilir.
   - Mevcut modelin eğitim sürecinde, hazır veri setlerinden yararlanarak doğruluk oranı artırılabilir.


<p>&nbsp;</p>

### KAYNAKLAR :
    - Projeye ait daha fazla video için : https://drive.google.com/drive/folders/1GmojXNA15YhoXZ7ysJKeXapwkATJ0xSp?usp=sharing
    - Beyazperde yorumlarından oluşturulmuş veri seti için : https://drive.google.com/file/d/1GpHxgiCukb5Lki76eWk072YjRBoUpXlG/view?usp=sharing
    - Denebunu yorumlarından oluşturulmuş veri seti için : https://drive.google.com/file/d/1k_6Bu4yLYaphWyZCK6ERaXh96bwoBFLz/view?usp=sharing

<p>&nbsp;</p> 

### SÜRÜMLER :
    - Python --> 3.9
    - Tensorflow --> 2.10.0
    - CUDA --> 11.8
    - CuDNN --> 8.6
    - SQLite --> 3.32.3
    - PyQt5 --> 5.15.11
    
