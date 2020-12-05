---
layout: post
title: Kaynak Konumlandırma
slug: source-localization
author: Bahri ABACI
categories:
- Makine Öğrenmesi
- Nümerik Yöntemler
- Veri Analizi
thumbnail: /assets/post_resources/source_localization/thumbnail.png
---
Kaynak konumlandırma (Source Localization), konumu bilinmeyen bir kaynağın, konumu bilinen refarans noktalarından alınan ölçümler sonucunda konumuna dair bir kestirimde bulunulması işlemidir. Biyomedikal görüntülemede beyne yerleştirilen elektrotlardan alınan sinyallerin şiddeti kullanılarak beyinde sinyali yayan bölgenin tespit edilmesi, akustik uygulamalarında mikrofon dizileri tarafından alınan sesin şiddetine bağlı olarak ses kaynağının tespiti gibi pek çok farklı uygulama alanına sahiptir. Bu yazımızda basit bir kaynak konumlandırma probleminin önceki yazılarımızda incelediğimiz [Gradyan İniş Yöntemleri]({% post_url 2020-04-08-gradyan-yontemleri-ile-optimizasyon %}) ile nasıl çözülebileceğini inceleyeceğiz.

<!--more-->

Kaynak konumlandırma başlık itibariyle hepimize uzak bir konu gibi görünse de aslında günlük hayatımızda da sıklıkla duyduğumuz bir kullanım alanına sahiptir. Örneğin kullandığımız cep telefonlarının konumu, herhangi bir ilave yazılım veya donanıma ihtiyaç duyulmadan bu yöntem ile tespit edilebilmektedir. Bu yazımızda inceleyeceğimiz örnek de anlaşılır olması açısından bu uygulama örneği üzerinden anlatılacaktır.

Örnek olarak, bir mobil telefon şirketinin bölgeye yerleştirdiği üç baz istasyonu (<img src="assets/post_resources/math//53d147e7f3fe6e47ee05b88b166bd3f6.svg?invert_in_darkmode" align=middle width=12.32879834999999pt height=22.465723500000017pt/>,<img src="assets/post_resources/math//61e84f854bc6258d4108d08d4c4a0852.svg?invert_in_darkmode" align=middle width=13.29340979999999pt height=22.465723500000017pt/> ve <img src="assets/post_resources/math//9b325b9e31e85137d1de765f43c0f8bc.svg?invert_in_darkmode" align=middle width=12.92464304999999pt height=22.465723500000017pt/>) olduğunu varsayalım. Konumu bulunmak istenen kullanıcının (<img src="assets/post_resources/math//cbfb1b2a33b28eab8a3e59464768e810.svg?invert_in_darkmode" align=middle width=14.908688849999992pt height=22.465723500000017pt/>) telefonu ile bölgeye girmesi durumunda, telefon ile üç baz istasyonu arasında bir iletişim kurulacak ve bu iletişim sonucunda baz istasyonları telefondan gelen sinyalin gücünü ölçebilecektir. Sinyalin gücü ile uzaklığı arasındaki ilişki kullanılarak kullanıcının üç baz istasyonuna olan uzaklıklarının (<img src="assets/post_resources/math//c6fd1ff85a70f0379388e065daa01f53.svg?invert_in_darkmode" align=middle width=15.68634539999999pt height=22.831056599999986pt/>, <img src="assets/post_resources/math//bfe0dfb83f2e22960a2d466927892bf0.svg?invert_in_darkmode" align=middle width=14.33680049999999pt height=22.831056599999986pt/> ve <img src="assets/post_resources/math//9ef2a63ebfdd240d9db00463889a4495.svg?invert_in_darkmode" align=middle width=14.43061619999999pt height=22.831056599999986pt/>) olarak belirli bir hata ile tahmin edildiğini varsayalım. Bu durum grafiksel olarak aşağıdaki şekilde görselleştirilmiştir.

![kaynak konumlandırma örnek#half][source_localization_example] 

Verilen problemde amacımız bilinen baz istasyonu konumları (<img src="assets/post_resources/math//4b1bf1e00b5819b7024d60ecfcba2368.svg?invert_in_darkmode" align=middle width=17.68403009999999pt height=22.465723500000017pt/>,<img src="assets/post_resources/math//2f58d43ed8079cf63f2df3cb116dd7e1.svg?invert_in_darkmode" align=middle width=16.33448519999999pt height=22.465723500000017pt/> ve <img src="assets/post_resources/math//d01a40270d2c05177752cd7114f55670.svg?invert_in_darkmode" align=middle width=16.42829924999999pt height=22.465723500000017pt/>) ve kestirilen uzaklıkları (<img src="assets/post_resources/math//c6fd1ff85a70f0379388e065daa01f53.svg?invert_in_darkmode" align=middle width=15.68634539999999pt height=22.831056599999986pt/>, <img src="assets/post_resources/math//bfe0dfb83f2e22960a2d466927892bf0.svg?invert_in_darkmode" align=middle width=14.33680049999999pt height=22.831056599999986pt/> ve <img src="assets/post_resources/math//9ef2a63ebfdd240d9db00463889a4495.svg?invert_in_darkmode" align=middle width=14.43061619999999pt height=22.831056599999986pt/>) kullanarak kullanıcının konumunu (<img src="assets/post_resources/math//3157862efb9cfe861b22a3ad1a9201c5.svg?invert_in_darkmode" align=middle width=18.00802079999999pt height=22.465723500000017pt/>) bulmaktır. Bu problem özelinde; baz istasyonu konumlarının <img src="assets/post_resources/math//cada15053201287bbacbdb9e425b3e1c.svg?invert_in_darkmode" align=middle width=76.95330884999998pt height=24.65753399999998pt/>, <img src="assets/post_resources/math//4dfac8c5dd457f2da339800cfc7ffcad.svg?invert_in_darkmode" align=middle width=75.60374579999998pt height=24.65753399999998pt/>, <img src="assets/post_resources/math//416d101a5a43a1cc487d2cbee57baf1f.svg?invert_in_darkmode" align=middle width=75.69758129999998pt height=24.65753399999998pt/> olduğunu ve kestirilen uzaklıkların <img src="assets/post_resources/math//466dc3a55490905174f233b7ef66dd01.svg?invert_in_darkmode" align=middle width=46.645099049999985pt height=22.831056599999986pt/>, <img src="assets/post_resources/math//ff5f3af7c4f708def950c26996aba306.svg?invert_in_darkmode" align=middle width=45.29553599999999pt height=22.831056599999986pt/>, <img src="assets/post_resources/math//ea813a03e6313fcd1d98bfb6b6a8f9b8.svg?invert_in_darkmode" align=middle width=45.38937149999999pt height=22.831056599999986pt/> şeklinde hesaplandığını varsayalım.

Verilen problem ilk bakışta üçgen eşitlikleri veya analitik yöntemler ile çözülebilir gibi görünse de, problemde bilinen <img src="assets/post_resources/math//2103f85b8b1477f430fc407cad462224.svg?invert_in_darkmode" align=middle width=8.55596444999999pt height=22.831056599999986pt/> mesafelerinin belirli bir hata ile kestirildiği unutulmamalıdır. Bu nedenle <img src="assets/post_resources/math//3157862efb9cfe861b22a3ad1a9201c5.svg?invert_in_darkmode" align=middle width=18.00802079999999pt height=22.465723500000017pt/> konumunda <img src="assets/post_resources/math//2103f85b8b1477f430fc407cad462224.svg?invert_in_darkmode" align=middle width=8.55596444999999pt height=22.831056599999986pt/> mesafesinin kestiriminden kaynaklanan bir hata olması muhtemeldir. Problemi optimizasyon problemi olarak yazarken amacımzı bu hatayı en küçükleyen <img src="assets/post_resources/math//369c616b8569848e51a7ff90fe49fdf9.svg?invert_in_darkmode" align=middle width=18.00802079999999pt height=31.141535699999984pt/> kestirimini bulmak olacaktır.

Problem tanımı gereği, <img src="assets/post_resources/math//5fbb629ed491bfde484b74a3dfdf21ea.svg?invert_in_darkmode" align=middle width=106.90334489999998pt height=24.65753399999998pt/>, <img src="assets/post_resources/math//3a9a5b245f9dbe2844aa9edc3514ec8f.svg?invert_in_darkmode" align=middle width=104.20423695pt height=24.65753399999998pt/> ve <img src="assets/post_resources/math//64c83f6f5059705fd139f0df63808981.svg?invert_in_darkmode" align=middle width=104.39188814999999pt height=24.65753399999998pt/> yazılabilir. Bu durumda herhangi bir <img src="assets/post_resources/math//df5a289587a2f0247a5b97c1e8ac58ca.svg?invert_in_darkmode" align=middle width=12.83677559999999pt height=22.465723500000017pt/> konumu için oluşacak ortalama karesel hata şu şekilde ifade edilebilir.

<p align="center"><img src="assets/post_resources/math//5ae471fd934a4622037bcd6a1ab16cf6.svg?invert_in_darkmode" align=middle width=207.55064549999997pt height=42.228991199999996pt/></p>

Verilen denklemde <img src="assets/post_resources/math//1662340dcdfbf9054c59657f976c3498.svg?invert_in_darkmode" align=middle width=61.25565764999999pt height=45.84475499999998pt/> problemde verilen bilinen noktaları göstermektedir. Denklem \ref{cost_function} ile verilen hata fonksiyonu incelendiğinde, fonksiyonun en küçük değerini <img src="assets/post_resources/math//71f954beb8237eff425707c11b05a20a.svg?invert_in_darkmode" align=middle width=52.76242289999999pt height=22.465723500000017pt/> olduğunda aldığı görülür. <img src="assets/post_resources/math//71f954beb8237eff425707c11b05a20a.svg?invert_in_darkmode" align=middle width=52.76242289999999pt height=22.465723500000017pt/> seçilmesi durumunda oluşan hata <img src="assets/post_resources/math//2103f85b8b1477f430fc407cad462224.svg?invert_in_darkmode" align=middle width=8.55596444999999pt height=22.831056599999986pt/> konum kestirim hatalarının karesel toplamının yarısı kadar olacaktır.

Problemin çözümü için <img src="assets/post_resources/math//bc6f778b34107ef9b9ce8952f48d7884.svg?invert_in_darkmode" align=middle width=35.43961904999999pt height=24.65753399999998pt/> fonksiyonu en küçükleyen <img src="assets/post_resources/math//ab4f6c2623fb8c960bf905eb57a6f78e.svg?invert_in_darkmode" align=middle width=143.12949419999998pt height=31.141535699999984pt/> noktasının bulunması gerekmektedir. Bu değer [Gradyan İniş Yöntemleri]({% post_url 2020-04-08-gradyan-yontemleri-ile-optimizasyon %}) ve [Lagrange Çarpanları]({% post_url 2020-01-13-lagrange-carpanlari-yontemi %}) yazılarımızda değindiğimiz üzere <img src="assets/post_resources/math//9b325b9e31e85137d1de765f43c0f8bc.svg?invert_in_darkmode" align=middle width=12.92464304999999pt height=22.465723500000017pt/> fonksiyonun gradyanını sıfıra eşitleyerek bulunur. Gradyan hesaplamasında kolaylık sağlaması açısından işlemlere başlamadan <img src="assets/post_resources/math//43f50433cca9b5d8f81ed17cd6d39839.svg?invert_in_darkmode" align=middle width=126.24604079999997pt height=24.65753399999998pt/> tanımlamasını yapalım. Bu tanım kullanılarak <img src="assets/post_resources/math//5eb3506cf8721a78598195593be1aa9b.svg?invert_in_darkmode" align=middle width=23.516088749999987pt height=22.831056599999986pt/> aşağıdaki şekilde yazılabilir.

<p align="center"><img src="assets/post_resources/math//03b142e8aee43760e6e69dc9b0ebc3a4.svg?invert_in_darkmode" align=middle width=301.52606384999996pt height=141.27060584999998pt/></p>

Elde edilen eşitlikten de görüldüğü üzere, hesaplamaya devam edebilmek için <img src="assets/post_resources/math//4674b5b7948b568ef09954609cfa725d.svg?invert_in_darkmode" align=middle width=38.935584599999984pt height=24.65753399999998pt/> fonksiyonunun gradyanına ihtiyaç duyulmaktadır. Bu hesaplama aşağıdaki şekilde yapılabilir.

<p align="center"><img src="assets/post_resources/math//83ff7cfa4117da4616ddfb594d8bf247.svg?invert_in_darkmode" align=middle width=469.97482125000005pt height=275.92431404999996pt/></p>

Denklem \ref{gradientg} ile elde edilen eşitlik Denklem \ref{gradientfclosed} da yerine konularsa;

<p align="center"><img src="assets/post_resources/math//32d6e882e740046ddb10221ba0a96e01.svg?invert_in_darkmode" align=middle width=360.2400978pt height=191.0373201pt/></p>

bulunur. Burada <img src="assets/post_resources/math//0e51a2dede42189d77627c4d742822c3.svg?invert_in_darkmode" align=middle width=14.433101099999991pt height=14.15524440000002pt/> verilen nokta sayısını (<img src="assets/post_resources/math//570d7243520fd2defc49258a573d3f60.svg?invert_in_darkmode" align=middle width=44.56994024999999pt height=21.18721440000001pt/>) göstermektedir. Bulunan <img src="assets/post_resources/math//48188cdca2f2d2d8e319f5884cb86214.svg?invert_in_darkmode" align=middle width=49.13829029999999pt height=24.65753399999998pt/> ifadesi kullanılarak, <img src="assets/post_resources/math//47aa36ae861c8c30c2d13445ef331f40.svg?invert_in_darkmode" align=middle width=51.80518364999998pt height=27.77565449999998pt/> seçilen [En Dik İniş Yöntemi]({% post_url 2020-04-08-gradyan-yontemleri-ile-optimizasyon %}) ile çözüm aşağıdaki şekilde hesaplanır.

<p align="center"><img src="assets/post_resources/math//7afad6f03f4fc4abe8957653521b9f88.svg?invert_in_darkmode" align=middle width=374.50445175pt height=131.63876714999998pt/></p>

Elde edilen iteratif çözümün gerçeklenmesi için C dilinde aşağıdaki kod parçası yazılmıştır.

```c
// set the given parameters
float Pi[3][2] = { {3.0f,9.0f}, {1.0f,1.0f}, {9.0f,2.0f} };
float di[3] = {6.0f, 4.0f, 5.0f};

// set the starting position of the X to somewhere
float x[2] = {0.0f};

// continue until the error is no more decreasing
float difference = 0;

do
{
    float xnew[2] = {0.0f};

    // compute \sum_{i \in S}  P_i + \sum_{i \in S}  d_i\frac{P_k - P_i}{\lVert P_k - P_i \lVert}
    int i = 0, j = 0;
    for(j = 0; j < n; j++)
    {
        for(i = 0; i < m; i++)
        {
            xnew[j] += (Pi[i][j] + di[i] * (x[j] - Pi[i][j]) / diffnorm(x, Pi[i], n)) / m;
        }
    }

    // now compute the difference between the xnew and x, and assign x = xn
    difference = diffnorm(x, xnew, n);
    memcpy(x, xnew, n * sizeof(float));
    
} while(difference > 1e-3);
```
Yazılan kod parçası <img src="assets/post_resources/math//1c6ed41be23457a20ec4fc6a9a767dc0.svg?invert_in_darkmode" align=middle width=76.37547389999999pt height=24.65753399999998pt/> ve <img src="assets/post_resources/math//76f83ec53790ea1a0f587eea812191fe.svg?invert_in_darkmode" align=middle width=92.81389259999999pt height=24.65753399999998pt/> gibi farklı iki başlangıç noktasından, elde edilen yeni konum <img src="assets/post_resources/math//8515c91e0dbc7b5fddaa59b96501ea0b.svg?invert_in_darkmode" align=middle width=34.46359784999999pt height=22.465723500000017pt/> ile eski konum <img src="assets/post_resources/math//fe63872d9f7a2e1fb98212c0037937f6.svg?invert_in_darkmode" align=middle width=17.81967659999999pt height=22.465723500000017pt/> arasındaki fark <img src="assets/post_resources/math//7478f3ddcc5c4a0d602772a3057efe42.svg?invert_in_darkmode" align=middle width=33.26498669999999pt height=26.76175259999998pt/> ten küçük olana kadar çalıştırıldığında, toplam <img src="assets/post_resources/math//da2d2542823daca235ebe489b76887bb.svg?invert_in_darkmode" align=middle width=16.438418699999993pt height=21.18721440000001pt/> adımda aşağıdaki görselde verilen adımları izleyerek <img src="assets/post_resources/math//698a73fa092332553b162526a233a181.svg?invert_in_darkmode" align=middle width=119.2865652pt height=24.65753399999998pt/> noktasına ulaşmaktadır.

|Başlangıç Noktası <img src="assets/post_resources/math//1c6ed41be23457a20ec4fc6a9a767dc0.svg?invert_in_darkmode" align=middle width=76.37547389999999pt height=24.65753399999998pt/> | Başlangıç Noktası <img src="assets/post_resources/math//76f83ec53790ea1a0f587eea812191fe.svg?invert_in_darkmode" align=middle width=92.81389259999999pt height=24.65753399999998pt/>|
|:-------:|:----:|
![kaynak konumlandırma örnek][source_localization_solution1] | ![kaynak konumlandırma örnek][source_localization_solution2]

Verilen grafiklerde, arka plan renkleri ve kontur çizgileri <img src="assets/post_resources/math//feecd8956177607fdd792bf009ecea8e.svg?invert_in_darkmode" align=middle width=72.88991324999999pt height=24.65753399999998pt/> seçilmesi durumunda elde edilecek hatayı göstermektedir. Siyah ile işaretlenen nokta iterasyonun başlangıç noktasını, kırmızı nokta ise iterasyonlar sonucunda ulaşılan noktayı göstermektedir. Turuncu ile gösterilen noktalar her iterasyon sonucunda gidilen yeni noktayı göstermektedir.

Yazıda yer alan analizlerin yapıldığı kod parçaları, görseller ve kullanılan veri setlerine [source_localization](https://github.com/cescript/source_localization) GitHub sayfası üzerinden erişilebilirsiniz.

**Referanslar**
* Beck, Amir. Introduction to nonlinear optimization: Theory, algorithms, and applications with MATLAB. Vol. 19. Siam, 2014.

[RESOURCES]: # (List of the resources used by the blog post)
[source_localization_example]: /assets/post_resources/source_localization/source_localization_example.svg
[source_localization_solution1]: /assets/post_resources/source_localization/source_localization_solution1.png
[source_localization_solution2]: /assets/post_resources/source_localization/source_localization_solution2.png