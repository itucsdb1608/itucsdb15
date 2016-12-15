from flask import Blueprint, render_template
from flask import current_app
from flask import request, session
from flask import redirect, url_for
from connect_db import add_message_to_table,get_messages_from_table,remove_message_from_table,update_one_message
from message import Message
from login import Person
from connect_db import add_hobby_to_table,get_hobby_from_table,remove_hobby_from_table,update_hobby_from_table
from connect_db import add_hobbyall_to_table,get_hobbyall_from_table,remove_hobbyall_from_table
from connect_db import add_ilgiall_to_table,get_ilgiall_from_table,remove_ilgiall_from_table
from connect_db import add_ilgi_to_table,get_ilgi_from_table,remove_ilgi_from_table,update_ilgi_from_table
from connect_db import add_profile_to_table,get_profile_from_table,remove_profile_from_table,update_profile_from_table
from profile import Profile
from connect_db import add_account_to_table,get_account_from_table,get_university_from_table,get_city_from_table,update_account_from_table,update_accountpersonal_from_table,add_accountpersonal_to_table,get_accountpersonal_from_table
from addaccount import Addaccount
from connect_db import add_to_login, records_from_login, update_to_login, remove_from_login, search_user_login
from connect_db import ekle_arkadas,tum_arkadaslar,gonder_username,toplam_arkadas,sil_arkadas,guncelle_arkadas
from friend import Friend
from connect_db import send_message,send_username_for_messages,update_personal_message,sil_kisisel_mesaj

site = Blueprint('site', __name__)
@site.route('/')
def home_page():
    return render_template('home.html')

@site.route('/signup', methods=['GET','POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('giris.html')
    else:
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        newRecord = Person(name, surname, email, username, password)
        newAccount = Addaccount(username, name, surname, email)
        add_to_login(newRecord)
        add_account_to_table(newAccount)
        add_accountpersonal_to_table(username)

    return render_template('home.html')

@site.route('/signin', methods=['GET','POST'])
def sign_in():
    if request.method == 'GET':
        return render_template('girisyap.html')
    else:
        username = request.form['username']
        password = request.form['password']
        check = search_user_login(username, password)
        if check == 1:
            session['name'] = username
            return redirect(url_for('site.signed_in'))
        else:
            return render_template('error.html')

@site.route('/cikis', methods=['GET'])
def cikis():
    session['name'] = ""
    return redirect(url_for('site.home_page'))


@site.route('/contactus')
def contact():
    return render_template('iletisim.html')

@site.route('/message/<int:messageId>/update',methods=['GET','POST'])
def update_message(messageId):
    if request.method == 'GET':
        return render_template('profile/update_message.html')
    else:
        content = request.form['content']
        subject = request.form['subject']
        update_one_message(content,subject,messageId)
        return redirect(url_for('site.signed_in'))

@site.route('/message/delete',methods=['GET','POST'])
def delete_message():
    if request.method == 'GET':
        return render_template('profile/index.html')
    else:
        id = request.form['delete']
        remove_message_from_table(id)
        return redirect(url_for('site.signed_in'))

@site.route('/message/add',methods=['GET','POST'])
def add_message():
    if request.method == 'GET':
        return render_template('profile/add_message.html')
    else:
        username = request.form['username']
        messageSubject = request.form['subject']
        messageContent = request.form['content']
        newMessage = Message(username,messageContent,messageSubject)
        add_message_to_table(newMessage)
        return redirect(url_for('site.signed_in'))

@site.route('/friends')
def friend_requests():
        return render_template('profile/arkadas.html')

@site.route('/friend/change', methods=['GET', 'POST'])      #arkadas.html in icinde kullanildi
def friend():
    if request.method == 'GET':
        return render_template('profile/arkadas.html')
    elif request.method == 'POST':
        if request.form['submit'] == 'Ekle':
            kullaniciadi = request.form['UserName']
            arkullaniciadi = request.form['FriendUserName']
            isim = request.form['FriendName']
            soyisim = request.form['FriendSurname']
            ekle_arkadas(kullaniciadi,arkullaniciadi,isim, soyisim)
            toplamarkadas = toplam_arkadas(kullaniciadi)
            tumu = gonder_username(kullaniciadi)
            username = kullaniciadi
          #  return redirect(url_for('site.friend_requests'))
            return render_template('profile/arkadas.html',arkadaslar = tumu , toplam = toplamarkadas ,  myusername = username  )
        elif request.form['submit'] == 'Duzenle':
            id = request.form['FriendID']
            isim = request.form['FriendName']
            soyisim = request.form['FriendSurname']
            duzenle_arkadas(id,isim,soyisim);
            return redirect(url_for('site.friend_requests'))
        elif request.form['submit'] == 'Sil':
            id = request.form['FriendID']
            sil_arkadas(id)
            return redirect(url_for('site.friend_requests'))
        elif request.form['submit'] == 'UsernameGonder':
            username = request.form['Username']
            tumu = gonder_username(username)
            toplamarkadas = toplam_arkadas(username)
           # tumu = tum_arkadaslar()
            return render_template('profile/arkadas.html',arkadaslar = tumu , toplam = toplamarkadas ) #olmazsa render ile dene



@site.route('/friend/ekle/<my>', methods=['GET', 'POST'])      #arkadas.html in icinde kullanildi
def friend_add(my):
    if request.method == 'GET':
        return render_template('profile/arkadas.html')
    elif request.method == 'POST':
        if request.form['submit'] == 'Ekle':

            arkullaniciadi = request.form['FriendUserName']
            isim = request.form['FriendName']
            soyisim = request.form['FriendSurname']
            ekle_arkadas(my,arkullaniciadi,isim, soyisim)
            toplamarkadas = toplam_arkadas(my)
            tumu = gonder_username(my)
            username = my
          #  return redirect(url_for('site.friend_requests'))
            return render_template('profile/arkadas.html',arkadaslar = tumu , toplam = toplamarkadas ,  myusername = username  )



@site.route('/friend/gonder', methods=['GET', 'POST'])      #arkadas.html in icinde kullanildi
def gonder_fr():
    if request.method == 'GET':
        return render_template('profile/arkadas.html')
    elif request.form['submit'] == 'UsernameGonder':
         username = request.form['Username']
         tumu = gonder_username(username)
         toplamarkadas = toplam_arkadas(username)
         # tumu = tum_arkadaslar()
         return render_template('profile/arkadas.html',arkadaslar = tumu , toplam = toplamarkadas , myusername = username )
        # return redirect(url_for('site.friend',arkadaslar = tumu , toplam = toplamarkadas ))
        # return render_template('profile/arkadas.html',arkadaslar = tumu , toplam = toplamarkadas ) #olmazsa render ile dene

@site.route('/friend/arkadasListesi')                       #arkadas.html in icinde kullanildi
def friend_listing():
     tumu = tum_arkadaslar()
     return render_template('profile/arkadas.html', arkadaslar = tumu)


@site.route('/friend/guncel/<my>', methods=['GET', 'POST'])
def friend_update(my):
    if request.method == 'GET':
        return render_template('profile/arkadas.html')
    elif request.method == 'POST':
        if request.form['submit'] == 'Guncelle':
            ad = my
            arkullaniciadi =  request.form['FriendUserName']
            yeniisim = request.form['FriendName']
            yenisoyisim = request.form['FriendSurname']
            guncelle_arkadas(ad, arkullaniciadi,yeniisim, yenisoyisim)
            toplamarkadas = toplam_arkadas(ad)
            tumu = gonder_username(ad)

          #  return redirect(url_for('site.friend_requests'))
            return render_template('profile/arkadas.html',arkadaslar = tumu , toplam = toplamarkadas ,  myusername = ad  )

@site.route('/friend/guncelle/<friendusername>/<myname>', methods=['GET', 'POST'])
def friend_real_update(friendusername , myname):
    if request.method == 'GET':
        return render_template('profile/arkadas.html')
    elif request.method == 'POST':
        if request.form['submit'] == 'Guncelle':
            ad = myname
            arkullaniciadi = friendusername
            yeniisim = request.form['FriendName']
            yenisoyisim = request.form['FriendSurname']
            guncelle_arkadas(ad, arkullaniciadi,yeniisim, yenisoyisim)
            toplamarkadas = toplam_arkadas(ad)
            tumu = gonder_username(ad)
            username = ad
          #  return redirect(url_for('site.friend_requests'))
            return render_template('profile/arkadas.html',arkadaslar = tumu , toplam = toplamarkadas ,  myusername = username  )

@site.route('/friend/sil/<username>/<myusername>', methods=['GET', 'POST'])
def friend_delete(username, myusername):
    if request.method == 'POST':
        a = username
        sil_arkadas(a)

        tumu = gonder_username(myusername)
        toplamarkadas = toplam_arkadas(myusername)
        return render_template('profile/arkadas.html',arkadaslar = tumu , toplam = toplamarkadas , myusername = myusername )
    else:
        return redirect(url_for('site.friend'))



@site.route('/un')
def usernamefr_requests():
        return render_template('profile/arkadasgiris.html')


@site.route('/signedin',methods=['GET', 'POST'])
def signed_in():
    if request.method == 'GET':
        messages = get_messages_from_table()
        return render_template('profile/index.html', messages = messages)
    else:
        return redirect(url_for('site.signed_in'))


@site.route('/admin/blog/<int:blog_id>/update',methods=['GET','POST'])
def update_blog(blog_id):
    if request.method == 'GET':
        return render_template('admin/blog_guncelle.html')
    else:
        title = request.form['title']
        content = request.form['content']
        update_profile_from_table(title,content,blog_id)
        return redirect(url_for('site.blog'))

@site.route('/admin/blog/delete',methods=['GET','POST'])
def delete_blog():
    if request.method == 'GET':
        return render_template('admin/blog.html')
    else:
        blog_id = request.form['delete']
        remove_profile_from_table(blog_id)
        return redirect(url_for('site.blog'))
@site.route('/admin/blog/add',methods=['GET','POST'])
def add_blog():
    if request.method == 'GET':
        return render_template('admin/blog_ekle.html')
    else:
        user_name = session['name']
        title = request.form['title']
        content = request.form['content']
        newProfile = Profile(user_name,title,content)
        add_profile_to_table(newProfile)
        return redirect(url_for('site.blog'))

@site.route('/admin/kisisel',methods=['GET','POST'])
def admin_kisisel():
    if request.method == 'GET':
        profile_account = get_account_from_table(session['name'])
        profile_university = get_university_from_table()
        profile_city = get_city_from_table()
        return render_template('admin/kisisel.html', profile_account = profile_account, profile_university= profile_university, profile_city=profile_city)
    else:
       ## usr_session = session['name']
            username    = request.form['username']
            ad          = request.form['ad']
            soyad       = request.form['soyad']
            resim       = request.form['resim']
            cinsiyet    = request.form['cinsiyet']
            universite  = request.form['universite']
            bolum       = request.form['bolum']
            giris       = request.form['giris']
            bitis       = request.form['bitis']
            dogum       = request.form['dogum']
            sehir       = request.form['sehir']
            eposta      = request.form['eposta']
            web         = request.form['web']
            update_account_from_table(username,ad,soyad,resim,cinsiyet,universite,bolum,giris,bitis,dogum,sehir,eposta,web)
            return redirect(url_for('site.admin_kisisel'))


@site.route('/admin/kisiselekbilgi',methods=['GET','POST'])
def admin_tanitma():
    if request.method == 'GET':
        profile_account = get_accountpersonal_from_table(session['name'])
        return render_template('admin/tanitma.html',  profile_account = profile_account)
    else:
        username    = request.form['username']
        hakkimda    = request.form['hakkimda']
        kod         = request.form['kod']
        sum1         = request.form['sum1']
        sum2        = request.form['sum2']
        sum3         = request.form['sum3']
        soz         = request.form['soz']
        lise         = request.form['lise']
        ort         = request.form['ort']
        update_accountpersonal_from_table(username,hakkimda,kod,sum1,sum2,sum3,soz,lise,ort)
        return redirect(url_for('site.admin_tanitma'))

@site.route('/admin/blog',methods=['GET', 'POST'])
def blog():
    if request.method == 'GET':
        profile_blog = get_profile_from_table(session['name'])
        return render_template('admin/blog.html', profile_blog = profile_blog)
    else:
        return redirect(url_for('site.blog'))



@site.route('/admin/hobi',methods=['GET', 'POST'])
def hobi():
    if request.method == 'GET':
        profile_blog = get_hobby_from_table()
        return render_template('admin/hobi.html', profile_blog = profile_blog)
    else:
        return redirect(url_for('site.hobi'))


@site.route('/admin/hobi/<int:hobby_id>/update',methods=['GET','POST'])
def update_hobi(hobby_id):
    if request.method == 'GET':
        return render_template('admin/hobi_guncelle.html')
    else:
        title = request.form['title']
        update_hobby_from_table(title,hobby_id)
        return redirect(url_for('site.hobi'))

@site.route('/admin/hobi/delete',methods=['GET','POST'])
def delete_hobi():
    if request.method == 'GET':
        return render_template('admin/hobi.html')
    else:
        hobby_id = request.form['delete']
        remove_hobby_from_table(hobby_id)
        return redirect(url_for('site.hobi'))
@site.route('/admin/hobi/add',methods=['GET','POST'])
def add_hobi():
    if request.method == 'GET':
        return render_template('admin/hobi_ekle.html')
    else:
        title = request.form['title']
        add_hobby_to_table(title)
        return redirect(url_for('site.hobi'))




@site.route('/admin/profilhobi',methods=['GET', 'POST'])
def profilhobi():
    if request.method == 'GET':
        profile_hobbyall = get_hobbyall_from_table(session['name'])
        return render_template('admin/profilhobi.html', profile_hobbyall = profile_hobbyall)
    else:
        return redirect(url_for('site.profilhobi'))

@site.route('/admin/profilhobi/delete',methods=['GET','POST'])
def delete_profilhobi():
    if request.method == 'GET':
        return render_template('admin/profilhobi.html')
    else:
        hobby_id = request.form['delete']
        remove_hobbyall_from_table(hobby_id)
        return redirect(url_for('site.profilhobi'))
@site.route('/admin/profilhobi/add',methods=['GET','POST'])
def add_profilhobi():
    if request.method == 'GET':
        profile_account = get_account_from_table(session['name'])
        profile_hobby = get_hobby_from_table()
        return render_template('admin/profilhobi_ekle.html', profile_account=profile_account, profile_hobby = profile_hobby)
    else:
        userid = request.form['userid']
        hobi = request.form['hobi']
        ord = request.form['ord']
        add_hobbyall_to_table(userid,hobi,ord)
        return redirect(url_for('site.profilhobi'))





@site.route('/admin/profililgi',methods=['GET', 'POST'])
def profililgi():
    if request.method == 'GET':
        profile_ilgiall = get_ilgiall_from_table(session['name'])
        return render_template('admin/profililgi.html', profile_ilgiall = profile_ilgiall)
    else:
        return redirect(url_for('site.profililgi'))

@site.route('/admin/profililgi/delete',methods=['GET','POST'])
def delete_profililgi():
    if request.method == 'GET':
        return render_template('admin/profililgi.html')
    else:
        ilgi_id = request.form['delete']
        remove_hobbyall_from_table(ilgi_id)
        return redirect(url_for('site.profililgi'))
@site.route('/admin/profililgi/add',methods=['GET','POST'])
def add_profililgi():
    if request.method == 'GET':
        profile_account = get_account_from_table(session['name'])
        profile_ilgi = get_ilgi_from_table()
        return render_template('admin/profililgi_ekle.html', profile_account=profile_account, profile_ilgi = profile_ilgi)
    else:
        userid = request.form['userid']
        ilgi = request.form['ilgi']
        ord = request.form['ord']
        add_ilgiall_to_table(userid,ilgi,ord)
        return redirect(url_for('site.profililgi'))







@site.route('/admin/ilgi',methods=['GET', 'POST'])
def ilgi():
    if request.method == 'GET':
        profile_blog = get_ilgi_from_table()
        return render_template('admin/ilgi.html', profile_blog = profile_blog)
    else:
        return redirect(url_for('site.ilgi'))


@site.route('/admin/ilgi/<int:ilgi_id>/update',methods=['GET','POST'])
def update_ilgi(ilgi_id):
    if request.method == 'GET':
        return render_template('admin/ilgi_guncelle.html')
    else:
        title = request.form['title']
        update_ilgi_from_table(title,ilgi_id)
        return redirect(url_for('site.ilgi'))

@site.route('/admin/ilgi/delete',methods=['GET','POST'])
def delete_ilgi():
    if request.method == 'GET':
        return render_template('admin/ilgi.html')
    else:
        ilgi_id = request.form['delete']
        remove_ilgi_from_table(ilgi_id)
        return redirect(url_for('site.ilgi'))
@site.route('/admin/ilgi/add',methods=['GET','POST'])
def add_ilgi():
    if request.method == 'GET':
        return render_template('admin/ilgi_ekle.html')
    else:
        title = request.form['title']
        add_ilgi_to_table(title)
        return redirect(url_for('site.ilgi'))






@site.route('/profile/<username>',methods=['GET','POST'])
def profile(username):
    if request.method == 'GET':
        profile_account     = get_account_from_table(username)
        if not profile_account:
            return redirect(url_for('site.home_page'))
        elif username not in profile_account[0]:
            return redirect(url_for('site.home_page'))
        profile_accountall  = get_accountpersonal_from_table(username)
        profile_hobbyall = get_hobbyall_from_table(username)
        profile_ilgiall = get_ilgiall_from_table(username)
        profile_blog        = get_profile_from_table(username)
        return render_template('profile/profil.html', profile_blog = profile_blog, profile_account=profile_account, profile_accountall=profile_accountall, profile_hobbyall=profile_hobbyall, profile_ilgiall=profile_ilgiall, )
    else:
        return redirect(url_for('site.    '))

@site.route('/messages')
def personel_message_request():
    return render_template('profile/mesaj.html')



@site.route('/aboutus')
def aboutus():
    records = records_from_login()
    return render_template('about.html', records = records)

@site.route('/user/remove', methods=['GET', 'POST'])
def remove_user():
    if request.method == 'GET':
        return render_template('about.html')
    else:
        user_id = request.form['delete']
        remove_from_login(user_id)
        records = records_from_login()
        return render_template('about.html', records = records)

@site.route('/user/update/', methods=['GET', 'POST'])
def update_user():
    if request.method == 'GET':
        return render_template('update.html')
    else:
        id = request.form['id_num']
        username = request.form['username']
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        updateRecord = Person(name, surname, email, username, password)
        update_to_login(id, updateRecord)
        records = records_from_login()
        return render_template('about.html', records = records)

@site.route('/admin/login')
def admin_login():
        return render_template('admin/login.html')

@site.route('/admin/home')
def admin_home():
        return render_template('admin/index.html')

@site.route('/messages')
def message_request():
        return render_template('profile/mesaj.html')


@site.route('/personalmessage/send/<my>', methods=['GET', 'POST'])
def personal_send(my):
    if request.method == 'GET':
        return render_template('profile/mesaj.html')
    elif request.method == 'POST':
        if request.form['submit'] == 'Add':

            touser = request.form['UserName']
            mesaj = request.form['PersonalContent']

            send_message(my,touser,mesaj)

            all = send_username_for_messages(my)
            username = my
            return render_template('profile/mesaj.html',bilgiler = all ,  myusername = username )


@site.route('/personalmessageupdate/<my>', methods=['GET', 'POST'])
def personal_message_update(my):
    if request.method == 'GET':
        return render_template('profile/mesaj.html')
    elif request.method == 'POST':
        if request.form['submit'] == 'Update':

            touser = request.form['UserName']
            mesaj = request.form['PersonalContent']

            update_personal_message(my,touser,mesaj)

            all = send_username_for_messages(my)
            username = my
            return render_template('profile/mesaj.html',bilgiler = all ,  myusername = username )




@site.route('/mesaj/gonder', methods=['GET', 'POST'])      #arkadas.html in icinde kullanildi
def take_username():
    if request.method == 'GET':
        return render_template('profile/mesaj.html')
    elif request.form['submit'] == 'Send':
         username = request.form['Username']
         all = send_username_for_messages(username)
         return render_template('profile/mesaj.html',bilgiler = all , myusername = username )


@site.route('/pmgiris')
def pmessage_request():
        return render_template('profile/mesajgiris.html')




@site.route('/mesaj/sil/<username>/<myusername>/<mesaj>', methods=['GET', 'POST'])
def personal_message_delete(username, myusername,mesaj):
    if request.method == 'POST':

        sil_kisisel_mesaj(username,mesaj)
        all = send_username_for_messages(myusername)

        return render_template('profile/mesaj.html',bilgiler = all , myusername = myusername )
    else:
        return redirect(url_for('site.message_request'))
