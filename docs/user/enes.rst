Parts Implemented by Hayati Enes Basat
======================================

Yönetici Paneli, Giriş ve Kaydol Sayfası
---------
Genel Bilgi
-------
Bu kısım kullanıcı için detaylı bilgi vermek amacıyla tasarlanmıştır. Sitenin görsellliği ve veri tabanı işlemleri ön planda tutulmaya çalışıldı.

Kaydol Sayfası 
http://itucsdb1608.mybluemix.net/signup
Giriş Yap Sayfası
http://itucsdb1608.mybluemix.net/signin
Yönetici bilgileri girildikten sonra yönetici paneli sayfası
http://itucsdb1608.mybluemix.net/administrator

Ayrıca normal üyelerin hakkında olan bir sayfa mevcuttur.
http://itucsdb1608.mybluemix.net/aboutus


Yönetici
-------
Sitedeki kullanıcı türlerinden biri de yönetici türüdür. Genel tanımla yönetici, sitedeki kullanıcı işlemleri üzerinde yetki sahibidir; yani yeni kullanıcı ekleyebilir veya kayıtlı kullanıcılar üzerinde silme veya güncelleme işlemleri yapabilir. Yönetici, normal kullanıcıların platform üzerinde yapabildiklerini de yapabilmektedir.

Yönetici Girişi
-------
Yönetici paneline erişebilmek için, giriş yap sayfasından kullanıcı adı ve parolasını girilmelidir. Ardından giriş yap butonuna tıklanır. Girilen bilgiler veri tabanındaki bilgilerle karşılaştırılır. Girilen bilgilere göre; bilgilerin yanlış olması durumunda hata sayfasına yönlendirilir. Girilen bilgiler normal yetkili kullanıcıya ait ise BeeLink Sosyal Platformuna geçerek ana sayfasına yönlendirilir. Girilen bilgiler yönetici yetkisinde kullanıcıya ait ise yönetici paneline yönlendirilir. Yönetici yetkisinde olmayan kullanıcılar yönetici paneline erişimi yoktur.

.. figure:: enes/1.PNG
   :figclass: align-center
   
   Giriş sayfasından yönetici girişi

Yönetici Ana Sayfa
-------
Yönetici giriş yaptıktan sonra yönetici paneli ana sayfasına yönlendirilir. İsterse yönetici hiçbir işlem yapmadan BeeLink Sosyal Platformuna kendi profiline geç butonuna basarak geçebilir veya çıkış yap butonuna basarak oturumu kapatabilir. Yönetici ana sayfasında site üzerinde kayıtlı tüm kullanıcıları, kullanıcıların bilgilerini ve kullanıcıların yetkilerini görebilir. Burada tüm kullanıcıları veri tabanından silebilme ve tüm kullanıcıların bilgilerini güncelleme yetkisine sahiptir. Yönetici, delete butonuna basarak seçtiği kullanıcıyı veri tabanından silebilir ve update butonuna basarak seçtiği kullanıcının bilgilerini güncelleyebilir. Eğer yönetici kendi üzerinde silme veya güncelleme işlemi yaparsa işlem yapılır ve oturum kapanarak giriş sayfasına yönlendirilir.

.. figure:: enes/2.PNG
   :figclass: align-center
   
   Yönetici paneli ana sayfa
   
Kullanıcı Ekleme
-------
Yönetici, yönetici ana sayfasından kullanıcı ekle butonuna basarak bu sayfaya geçiş yapar. Kullanıcı ekle butonuna basarak ekleme sayfasına geçebilir. Bu sayfa üzerinde ekleyeceği kullanıcının bilgilerini girerek sisteme yeni bir kullanıcı ekleyebilir.

.. figure:: enes/3.PNG
   :figclass: align-center
   
   Yönetici panelinden kullanıcı ekleme sayfası
 
 Burada, yönetici ekleyeceği kullanıcının yetkisini seçer. Ekleyeceği kullanıcı yönetici veya normal kullanıcı yetkisinde olabilir. Bu buton üzerinde değişiklik yapılmazsa varsayılan olarak kullanıcı olarak eklenir. Eğer ekleyeceği kullanıcının yetkisinde değişiklik yapmak istiyorsa üzerine tıklar.
 
.. figure:: enes/4.PNG
   :figclass: align-center
   
   Yönetici panelinden eklenecek kullanıcının yetkisini ayarlama

Yönetici, eklenecek kullanıcının yetkisini ayarladıktan sonra bilgilerini girer ve kaydet butonuna basarak yeni kullanıcı veri tabanına eklenmiş olur ve ardından yönetici ana sayfasına yönlendirilir.

Kullanıcı Güncelleme
-------
Yönetici, yönetici ana sayfasından istediği kullanıcı üzerinde güncelleme işlemi yapabilir. Seçtiği kullanıcının yanındaki update butonuna basarak güncelleme sayfasına yönlendirilir.

.. figure:: enes/5.PNG
   :figclass: align-center
   
   Yönetici panelinden kullanıcı güncelleme

Yönetici buradan, güncellemek istediği kullanıcının kullanıcı adını, ismini, soyismini, e-posta adresini, ve parolasını girer ve update butonuna basarak kullanıcı bilgileri güncellenir ve yönetici ana sayfasına yönlendirilir.

Yönetici Notları
-------
Yönetici sayfa üzerinden notlarım butonuna basarak notlarını görüntüleyebilir veya not ekle butonuna basarak yeni not ekleyebilir. Fakat yönetici sadece kendi yönetici notları üzerinde yetkisi vardır. Diğer yöneticilerin notlarını göremez ve üzerlerinde herhangi bir işlem yetkisine sahip değildir. Burada yönetici delete butonuna basarak notlarından birini seçerek silebilir veya update butonuna basarak notlarından birini seçerek güncelleyebilir.

.. figure:: enes/6.PNG
   :figclass: align-center
   
   Yönetici paneli üzerindeki notlar 
   
Yönetici not eklemek istiyorsa not ekle butonuna basarak not ekleme sayfasına yönlendirilir. Yönetici eklemek istediği notu girerek kaydet butonuna basarak işlem tamamlanır, veri tabanında güncellenir ve notlarım sayfasına yönlendirilir.

.. figure:: enes/7.PNG
   :figclass: align-center
   
   Yönetici panelinden not ekleme

Yönetici notunu güncellemek istiyorsa notlarım sayfasındaki seçtiği bir not üzerinde update butonuna basarak not güncelleme sayfasına yönlendirilir. Ardından girdiği bilgileri kaydet butonuna basarak güncelleme işlemi tamamlanmış olur.

.. figure:: enes/8.PNG
   :figclass: align-center
   
   Yönetici panelinden not güncelleme

Kullanıcı Giriş ve Kaydol İşlemleri
---------

Kaydol
-------
Kullanıcı, BeeLink ana sayfası üzerinden kaydol butonuna basarak kaydolma işlemini başlatabilir.

.. figure:: enes/9.PNG
   :figclass: align-center
   
   BeeLink ana sayfası ve kaydol butonu

Bu sayfa üzerinde bilgilerini girerek kaydolabilir. İsim, soyisim, e-posta adresi, kullanıcı adı ve parola parametrelerini girildikten sonra, kaydol butonuna basarak kayıt tamamlanır ve BeeLink ana sayfasına yönlendirilir.

.. figure:: enes/10.PNG
   :figclass: align-center
   
   BeeLink kaydol sayfası

Giriş Yap
-------
Kullanıcı BeeLink ana sayfası üzerinde giriş yap butonuna basarak giriş yapma sayfasına yönlendirilir.

Sosyal platforma erişebilmek için, giriş yap sayfasından kullanıcı adı ve parolasını girilmelidir. Ardından giriş yap butonuna tıklanır. Girilen bilgiler veri tabanındaki bilgilerle karşılaştırılır. Girilen bilgilere göre; bilgilerin yanlış olması durumunda hata sayfasına yönlendirilir. Girilen bilgiler ait ise BeeLink Sosyal Platformuna geçerek ana sayfasına yönlendirilir.

.. figure:: enes/11.PNG
   :figclass: align-center
   
   Giriş sayfasından kullanıcı girişi
