#include <Ethernet.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include <MFRC522.h>
////////////////////////   Sensor de Temperatura /////////////////////////
#include <Wire.h>
#include <Adafruit_MLX90614.h>
#define I2C_ADDR 0x27 //I2C adress
/////////////////////////////////////////////////////////////////


#define RST_PIN         0           // (D1)Configurable, see typical pin layout above
#define SS_PIN          2
MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;
LiquidCrystal_I2C lcd(0x27, 16, 2);
////////////////// Variables Globales temperatura
Adafruit_MLX90614 mlx = Adafruit_MLX90614();
float TO = 0;
float Promedio_tem = 0;
float Tem_ajustada = 0;
float TO1 = 0;
int divisor  = 0;
/////////////////////////////////////////////////////////////////////////////////////////////////////////
// Configuraciones Importantes Wifi//////////////////////////////////////////////////////////////////////
//String ssid ="Internet_UNL"; //nombre de la red a la que se va a conectar/////////////////////////////
//String password="UNL1859WiFi"; //contraseña de la red a la que se va a conectar https://odoo-105563-0.cloudclusters.net/////////////////////

String ssid ="Xtrim_Sebastian"; //nombre de la red a la que se va a conectar/////////////////////////////
String password="LUCAS2662lc";


//Configuraciones de acceso
//String pass = "34AW";    ///////////////////////////////CONTRASEÑA DE SEGURIDAD DEL APARATO, DEBE SER LA MISMA REGISTRADA EN EL SISTEMA WEB/////////////////////////////////////////////////////////
String lab = "1";       //NOMBRE DEL LABORATORIO A MOSTRAR EN LA PATALLA
String dominio = "http://192.168.3.11:8069";
String host = dominio + "/api/dost";
String hostPuerta = dominio + "/api/dost/abrirPuerta";

String puerta = "http://10.10.185.140:8069/api/dost/abrir";
String maestra = "03 FE DB 18"; //CLAVE DE LA LLAVE MAESTRA PARA APERTURAR EN CASO DE QUE NO HAYA INTERNET (ACTUALIZACIÓN Y REGISTRO MANUAL)
long Tiempo_abrir_puerta = 2000;
//////////////////////////////
/////FIN CONFIGURACIONES///////
unsigned long lastTime = 0;
// Timer set to 10 minutes (600000)
//unsigned long timerDelay = 600000;
// Set timer to 5 seconds (5000)
unsigned long timerDelay = 5000;
unsigned long TiempoActual, ConsultarPuerta;
/////////////////////////////////////////////////////////////////////7
//#define Rele D0
int Rele = 16;         /// Pin 8 de Rele
void setup() {
  lcd.init();
  lcd.backlight();         //enciende la pantalla LCD
  Serial.begin(9600);
  mlx.begin();
  while (!Serial)
  {
    // Nothing here. Just wait for serial to be present
  }
  SPI.begin();

  pinMode(Rele, OUTPUT);
  digitalWrite(Rele, LOW); //LÓGICA INVERSA

  WiFi.begin(ssid, password);
  bool salir = true;
  unsigned long TiempoAc = millis();
  while (WiFi.status() != WL_CONNECTED && salir == true) {
    Serial.println("CONECTANDO");
    MensajeCarga("CONECTANDO");
    if (millis() > (TiempoAc + 7000))
      salir = false;
    delay (5000);
  };
  TiempoActual = millis();
  if (WiFi.status() == WL_CONNECTED)MensajeLCD("CONECTADO CON IP", WiFi.localIP().toString());
  else MensajeLCD("NO CONECTADO", "...");
  while (millis() < TiempoActual + 2000) {};
  while (!Serial)
  {
    // Nothing here. Just wait for serial to be present
  }
  SPI.begin();
  mfrc522.PCD_Init();
  // Just wait some seconds...
  delay(4);
  // Prepare the security key for the read and write functions.
  // Normally it is 0xFFFFFFFFFFFF
  // Note: 6 comes from MF_KEY_SIZE in MFRC522.h
  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF; //keyByte is defined in the "MIFARE_Key" 'struct' definition in the .h file of the library
  }
  MensajeLCD("ACERQUE SU", "TARJETA");
  ConsultarPuerta = millis();
}

void loop() {
  
  
  if (WiFi.status() == WL_CONNECTED) {
    abrirPuertaRemotamente();
    Serial.println("///////////////////////////////////////////////");
    delay(5000);
    //String Id = ObtenerTag();
    if (!mfrc522.PICC_IsNewCardPresent()) {
      return;
    }
    // Select one of the cards. This returns false if read is not successful; and if that happens, we stop the code
    if (!mfrc522.PICC_ReadCardSerial()) {
      return;
    }
    // At this point, the serial can be read. We transform from byte to hex
    String serial = "";
    for (int x = 0; x < mfrc522.uid.size; x++)
    {
      Serial.println("Entro en el for");
      // If it is less than 10, we add zero
      if (mfrc522.uid.uidByte[x] < 0x10)
      {
        serial += "0";
      }
      // Transform the byte to hex
      serial += String(mfrc522.uid.uidByte[x], HEX);
      // Add a hypen
      if (x + 1 != mfrc522.uid.size)
      {
        serial += " ";
      }
    }
    // Transform to uppercase

    //   lecturaTemperatura();/////////////////  ojo
    Serial.println("Serial antes del toUpercase:" + serial);
    serial.toUpperCase();


    Serial.println("Read serial is: " + serial);

    if(serial == maestra){
      MensajeLCD("BIENVENIDO", "PASE");
        puerta_a();
        delay(1000);
        MensajeLCD("ACERQUE SU", "TARJETA");
      }else{
        /////
        WiFiClient client;
    HTTPClient http;
    String Enviar = "pass=" + serial + "&lab=" + lab;
    Serial.println("Esto se envia:" + Enviar);
    http.begin(client, host);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    int codigo_respuesta = http.POST(Enviar);
    if (codigo_respuesta > 0) {
      Serial.println("Codigo respuesta puerta:" + String(codigo_respuesta));
      if (codigo_respuesta == 200) {
        String cuerpo = http.getString();
        Serial.println("Codigo cuerpo:" + cuerpo);
        if (cuerpo == "registrar temperatura") {

          MensajeLCD("TOMAR", "TEMPERATURA");
          delay(5000);
          lecturaTemperatura();

          String Enviar2 = "lab=" + lab + "&Temperatura=" + Promedio_tem + "&pass=" + serial;
          Serial.println(Enviar2);
          //////////////////////////////////////////
          if (isnan(Promedio_tem)) {
            MensajeLCD("ACCESO", "DENEGADO");
          delay(2000);
          MensajeLCD("NO SE DETECTO", "TEMPERATURA");
          }else{
             http.begin(client, host);
          http.addHeader("Content-Type", "application/x-www-form-urlencoded");
          int codigo_respuesta = http.POST(Enviar2);
          String message = http.getString();
          Serial.println("Mesaage:" + message);
          
          if (Promedio_tem < 38) {
            String mystring;

            mystring = String(Promedio_tem);
            MensajeLCD("BIENVENIDO PASE", message);
            delay(2000);
            MensajeLCD("TEMPERATURA:", mystring);
            Serial.println(Promedio_tem);
            puerta_a();
          } else {
            String mystring;
            mystring = String(Promedio_tem);
            MensajeLCD("ACCESO", "DENEGADO");
            delay(2000);
            MensajeLCD("POR TEMPERATURA ALTA:", mystring);
          }

            
}

         


        } 
        else {
          abrirPuertaAdmin();
          MensajeLCD("ACCESO", "DENEGADO");
          delay(2000);
          MensajeLCD("HORARIO NO", "RESPECTIVO");
          
        }

        // http.end();
        // delay(50000);
        delay(1000);
        MensajeLCD("ACERQUE SU", "TARJETA");

        ////
      }
    

      }
      else {
        Serial.println("Codigo cuerpo:");
      }
    }

    // Halt PICC
    mfrc522.PICC_HaltA();
    // Stop encryption on PCD
    mfrc522.PCD_StopCrypto1();

    
   
    
  }
  else {
    abrirPuertaAdmin();
    delay(1000);
    MensajeLCD("CONEXION PERDIDA", "RECONECTANDO..");
    delay(1000);
    /*String Id = ObtenerTag();
    if (Id != "") {
      if (Id == maestra) {
        digitalWrite(Rele, HIGH);
        TiempoActual = millis();
        delay(Tiempo_abrir_puerta);
        digitalWrite(Rele, LOW);
      }
    }*/
  }

}




void MensajeCarga(String Lin1) {
  String Serie = "";
  lcd.clear();          //limpiamos la pantalla lcd
  lcd.print(Lin1);      //imprimimos la primera línea en pantalla lcd
  Serial.println(Lin1);
  TiempoActual = millis();                 //tomamos el tiempo actual
  unsigned long TiempoRespaldo;
  while (millis() < TiempoActual + 1000) {
    if (Serie.length() % 16 == 0)
    {
      Serie = "                ";
      lcd.setCursor(0, 1);  //ubicamos el cursor en la segunda fila
      lcd.print(Serie);
      Serie = "";
    }
    TiempoRespaldo = millis();
    while (millis() < TiempoRespaldo + 30) {};
    Serie = Serie + ".";
    Serial.println(Serie);
    lcd.setCursor(0, 1);  //ubicamos el cursor en la segunda fila
    lcd.print(Serie);      //imprimimos la segunda línea en pantalla lcd
  }
}


String ReemplazaCaracteres(String cadena) {
  cadena.replace("á", "a");
  cadena.replace("é", "e");
  cadena.replace("í", "i");
  cadena.replace("ó", "o");
  cadena.replace("ú", "u");
  cadena.replace("Á", "A");
  cadena.replace("É", "E");
  cadena.replace("Í", "I");
  cadena.replace("Ó", "O");
  cadena.replace("Ú", "U");
  cadena.replace("ñ", "n");
  cadena.replace("Ñ", "N");
  return cadena;
}

void MensajeLCD(String Lin1, String Lin2) { //función para mostrar los mensajes en la pantalla lcd,
  //recibe 2 Strings para colocarlos en cada fila de la pantalla respectivamente.

  Lin1 = ReemplazaCaracteres(Lin1); //Reemplazamos caracteres especiales.
  Lin2 = ReemplazaCaracteres(Lin2); //Reemplazamos caracteres especiales.
  lcd.clear();          //limpiamos la pantalla lcd
  lcd.setCursor(0, 0);
  lcd.print(Lin1);      //imprimimos la primera línea en pantalla lcd
  lcd.setCursor(0, 1);  //ubicamos el cursor en la segunda fila
  lcd.print(Lin2);      //imprimimos la segunda línea en pantalla lcd
  Serial.println(Lin1 + " " + Lin2);
}

void lecturaTemperatura() {

  for (int i = 0; i < 21; i++) {

    TO = mlx.readObjectTempC();

    if ((TO > 25 && TO < 41)) {
      divisor++;
      TO = mlx.readObjectTempC();
      Serial.print("entro 1");
      delay(10);

      Serial.print("N.lectura= ");
      Serial.print(i);
      Serial.print("  ");
      Serial.print(TO);
      TO1 = TO + TO1;
      Serial.print("   ");
      Serial.println(TO1);
      delay(1);
    }
    if ((TO < 25)) {
      MensajeLCD("COLOQUE SU", "MANO");
      delay(1000);
    }
  }
  Promedio_tem = (TO1 / divisor) + 10.0;
  Serial.print("Promedio=");
  Serial.println(Promedio_tem);
  delay(50);
  divisor = 0;
  TO1 = 0;
  TO = 0;
}

void puerta_a() {
  Serial.print("Abrio Puerta");
  digitalWrite(Rele, HIGH);
  delay(4000);
  digitalWrite(Rele, LOW);

}




void abrirPuertaRemotamente() {
   Serial.println("abrir puerta remotamente3");
  String estado = "cerrado";
  WiFiClient client;
  HTTPClient http;
  String Enviar = "estado=" + estado + "&lab=" + lab;
  Serial.println("Esto se envia:" + Enviar);
  http.begin(client, hostPuerta);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  int codigo_respuesta = http.POST(Enviar);
  if (codigo_respuesta > 0) {
    Serial.println("Codigo respuesta puerta:" + String(codigo_respuesta));
    if (codigo_respuesta == 200) {
      String cuerpo = http.getString();
      Serial.println("Codigo cuerpo:" + cuerpo);
      if (cuerpo == "abrir puerta") {

        MensajeLCD("BIENVENIDO", "PASE");
        puerta_a();
        delay(1000);
        MensajeLCD("ACERQUE SU", "TARJETA");



      } else{
        delay(1000);
        //MensajeLCD("INGRESE SU", "TARJETA");
        return;
      }
      

    }
  }
}

void abrirPuertaAdmin() {
  Serial.println("ingreso al metodo avrir puerta con tarjeta del admin");
  if (!mfrc522.PICC_IsNewCardPresent()) {
      return;
    }
    if (!mfrc522.PICC_ReadCardSerial()) {
      return;
    }
    String serial = "";
    for (int x = 0; x < mfrc522.uid.size; x++)
    {
      Serial.println("Entro en el for");
      if (mfrc522.uid.uidByte[x] < 0x10)
      {
        serial += "0";
      }
      serial += String(mfrc522.uid.uidByte[x], HEX);
      
      if (x + 1 != mfrc522.uid.size)
      {
        serial += " ";
      }
    }
    
    serial.toUpperCase();

    if(serial == maestra){
      MensajeLCD("BIENVENIDO", "PASE");
        puerta_a();
        delay(1000);
      }else{
        delay(1000);
        return;
      }
  
}
