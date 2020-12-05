---
layout: post
title: Kaynak Konumlandırma (Source Localization)
author: Bahri ABACI
categories:
- Makine Öğrenmesi
- Nümerik Yöntemler
- Veri Analizi
thumbnail: /assets/post_resources/source_localization/thumbnail.png
---
Kaynak konumlandırma (Source Localization), konumu bilinmeyen bir kaynağın, konumu bilinen refarans noktalarından alınan ölçümler sonucunda konumuna dair bir kestirimde bulunulması işlemidir. Biyomedikal görüntülemede beyne yerleştirilen elektrotlardan alınan sinyallerin şiddeti kullanılarak beyinde sinyali yayan bölgenin tespit edilmesi, akustik uygulamalarında mikrofon dizileri tarafından alınan sesin şiddetine bağlı olarak ses kaynağının tespiti gibi pek çok farklı uygulama alanına sahiptir. Bu yazımızda basit bir kaynak konumlandırma probleminin önceki yazılarımızda incelediğimiz [Gradyan İniş Yöntemleri]({% post_url 2020-04-08-gradyan-yontemleri-ile-optimizasyon-optimization-using-gradient-methods %}) ile nasıl çözülebileceğini inceleyeceğiz.

<!--more-->

Kaynak konumlandırma başlık itibariyle hepimize uzak bir konu gibi görünse de aslında günlük hayatımızda da sıklıkla duyduğumuz bir kullanım alanına sahiptir. Örneğin kullandığımız cep telefonlarının konumu, herhangi bir ilave yazılım veya donanıma ihtiyaç duyulmadan bu yöntem ile tespit edilebilmektedir. Bu yazımızda inceleyeceğimiz örnek de anlaşılır olması açısından bu uygulama örneği üzerinden anlatılacaktır.

Örnek olarak, bir mobil telefon şirketinin bölgeye yerleştirdiği üç baz istasyonu (!["A"](https://render.githubusercontent.com/render/math?math=A),!["B"](https://render.githubusercontent.com/render/math?math=B) ve !["C"](https://render.githubusercontent.com/render/math?math=C)) olduğunu varsayalım. Konumu bulunmak istenen kullanıcının (!["X"](https://render.githubusercontent.com/render/math?math=X)) telefonu ile bölgeye girmesi durumunda, telefon ile üç baz istasyonu arasında bir iletişim kurulacak ve bu iletişim sonucunda baz istasyonları telefondan gelen sinyalin gücünü ölçebilecektir. Sinyalin gücü ile uzaklığı arasındaki ilişki kullanılarak kullanıcının üç baz istasyonuna olan uzaklıklarının (!["d_a"](https://render.githubusercontent.com/render/math?math=d_a), !["d_b"](https://render.githubusercontent.com/render/math?math=d_b) ve !["d_c"](https://render.githubusercontent.com/render/math?math=d_c)) olarak belirli bir hata ile tahmin edildiğini varsayalım. Bu durum grafiksel olarak aşağıdaki şekilde görselleştirilmiştir.

![kaynak konumlandırma örnek#half][source_localization_example] 

Verilen problemde amacımız bilinen baz istasyonu konumları (!["P_a"](https://render.githubusercontent.com/render/math?math=P_a),!["P_b"](https://render.githubusercontent.com/render/math?math=P_b) ve !["P_c"](https://render.githubusercontent.com/render/math?math=P_c)) ve kestirilen uzaklıkları (!["d_a"](https://render.githubusercontent.com/render/math?math=d_a), !["d_b"](https://render.githubusercontent.com/render/math?math=d_b) ve !["d_c"](https://render.githubusercontent.com/render/math?math=d_c)) kullanarak kullanıcının konumunu (!["P_x"](https://render.githubusercontent.com/render/math?math=P_x)) bulmaktır. Bu problem özelinde; baz istasyonu konumlarının !["P_a=(3,9)"](https://render.githubusercontent.com/render/math?math=P_a%3d%283%2c9%29), !["P_b=(1,1)"](https://render.githubusercontent.com/render/math?math=P_b%3d%281%2c1%29), !["P_c=(9,2)"](https://render.githubusercontent.com/render/math?math=P_c%3d%289%2c2%29) olduğunu ve kestirilen uzaklıkların !["d_a=6"](https://render.githubusercontent.com/render/math?math=d_a%3d6), !["d_b=4"](https://render.githubusercontent.com/render/math?math=d_b%3d4), !["d_c=5"](https://render.githubusercontent.com/render/math?math=d_c%3d5) şeklinde hesaplandığını varsayalım.

Verilen problem ilk bakışta üçgen eşitlikleri veya analitik yöntemler ile çözülebilir gibi görünse de, problemde bilinen !["d"](https://render.githubusercontent.com/render/math?math=d) mesafelerinin belirli bir hata ile kestirildiği unutulmamalıdır. Bu nedenle !["P_x"](https://render.githubusercontent.com/render/math?math=P_x) konumunda !["d"](https://render.githubusercontent.com/render/math?math=d) mesafesinin kestiriminden kaynaklanan bir hata olması muhtemeldir. Problemi optimizasyon problemi olarak yazarken amacımzı bu hatayı en küçükleyen !["\hat{X}"](https://render.githubusercontent.com/render/math?math=%5chat%7bX%7d) kestirimini bulmak olacaktır.

Problem tanımı gereği, !["\lVert P_a-P_x \lVert \approx d_a"](https://render.githubusercontent.com/render/math?math=%5clVert%20P_a-P_x%20%5clVert%20%5capprox%20d_a), !["\lVert P_b-P_x \lVert \approx d_b"](https://render.githubusercontent.com/render/math?math=%5clVert%20P_b-P_x%20%5clVert%20%5capprox%20d_b) ve !["\lVert P_c-P_x \lVert \approx d_c"](https://render.githubusercontent.com/render/math?math=%5clVert%20P_c-P_x%20%5clVert%20%5capprox%20d_c) yazılabilir. Bu durumda herhangi bir !["P"](https://render.githubusercontent.com/render/math?math=P) konumu için oluşacak ortalama karesel hata şu şekilde ifade edilebilir.

!["f(P) = \frac{1}{2} \sum_{i \in S} (\lVert P-P_i \lVert - d_i)^2 \label{cost_function} \tag{1}"](https://render.githubusercontent.com/render/math?math=f%28P%29%20%3d%20%5cfrac%7b1%7d%7b2%7d%20%5csum_%7bi%20%5cin%20S%7d%20%28%5clVert%20P-P_i%20%5clVert%20-%20d_i%29%5e2)

Verilen denklemde !["S=\{ a,b,c\}"](https://render.githubusercontent.com/render/math?math=S%3d%5c%7b%20a%2cb%2cc%5c%7d) problemde verilen bilinen noktaları göstermektedir. Denklem \ref{cost_function} ile verilen hata fonksiyonu incelendiğinde, fonksiyonun en küçük değerini !["P=P_x"](https://render.githubusercontent.com/render/math?math=P%3dP_x) olduğunda aldığı görülür. !["P=P_x"](https://render.githubusercontent.com/render/math?math=P%3dP_x) seçilmesi durumunda oluşan hata !["d"](https://render.githubusercontent.com/render/math?math=d) konum kestirim hatalarının karesel toplamının yarısı kadar olacaktır.

Problemin çözümü için !["C(P)"](https://render.githubusercontent.com/render/math?math=C%28P%29) fonksiyonu en küçükleyen !["\hat{P_x} = \arg \min_{P} f(P)"](https://render.githubusercontent.com/render/math?math=%5chat%7bP_x%7d%20%3d%20%5carg%20%5cmin_%7bP%7d%20f%28P%29) noktasının bulunması gerekmektedir. Bu değer [Gradyan İniş Yöntemleri]({% post_url 2020-04-08-gradyan-yontemleri-ile-optimizasyon-optimization-using-gradient-methods %}) ve [Lagrange Çarpanları]({% post_url 2020-01-13-lagrange-carpanlari-yontemi-lagrange-multipliers %}) yazılarımızda değindiğimiz üzere !["C"](https://render.githubusercontent.com/render/math?math=C) fonksiyonun gradyanını sıfıra eşitleyerek bulunur. Gradyan hesaplamasında kolaylık sağlaması açısından işlemlere başlamadan !["g_i(P) = \lVert P-P_i \lVert"](https://render.githubusercontent.com/render/math?math=g_i%28P%29%20%3d%20%5clVert%20P-P_i%20%5clVert) tanımlamasını yapalım. Bu tanım kullanılarak !["\nabla f"](https://render.githubusercontent.com/render/math?math=%5cnabla%20f) aşağıdaki şekilde yazılabilir.

!["\begin{aligned}    \nabla f(P)&=\nabla \left ( \frac{1}{2} \sum_{i \in S} \left ( g_i(P) -d_i \right )^2 \right )\\    &= \sum_{i \in S} \nabla g_i(P) \left ( g_i(P) -d_i \right )\\    &= \sum_{i \in S} \nabla g_i(P) g_i(P) - \sum_{i \in S}  \nabla g_i(P) d_i\end{aligned}\label{gradientfclosed} \tag{2}"](https://render.githubusercontent.com/render/math?math=%5cbegin%7baligned%7d%20%20%20%20%5cnabla%20f%28P%29%26%3d%5cnabla%20%5cleft%20%28%20%5cfrac%7b1%7d%7b2%7d%20%5csum_%7bi%20%5cin%20S%7d%20%5cleft%20%28%20g_i%28P%29%20-d_i%20%5cright%20%29%5e2%20%5cright%20%29%5c%5c%20%20%20%20%26%3d%20%5csum_%7bi%20%5cin%20S%7d%20%5cnabla%20g_i%28P%29%20%5cleft%20%28%20g_i%28P%29%20-d_i%20%5cright%20%29%5c%5c%20%20%20%20%26%3d%20%5csum_%7bi%20%5cin%20S%7d%20%5cnabla%20g_i%28P%29%20g_i%28P%29%20-%20%5csum_%7bi%20%5cin%20S%7d%20%20%5cnabla%20g_i%28P%29%20d_i%5cend%7baligned%7d%5clabel%7bgradientfclosed%7d%20%5ctag%7b2%7d)

Elde edilen eşitlikten de görüldüğü üzere, hesaplamaya devam edebilmek için !["g_i(P)"](https://render.githubusercontent.com/render/math?math=g_i%28P%29) fonksiyonunun gradyanına ihtiyaç duyulmaktadır. Bu hesaplama aşağıdaki şekilde yapılabilir.

!["\begin{aligned}    \nabla g_i(P)&= \nabla \lVert P - P_i \lVert\\    &= \nabla \left( \sum_{j=1}^n \left ( P_j - P_{ij} \right )^2 \right)^{\frac{1}{2}}\\    &= \frac{1}{2} \left( \sum_{j=1}^n \left ( P_j - P_{ij} \right )^2 \right)^{-\frac{1}{2}} \left( \sum_{j=1}^n 2(P_j - P_{ij}) \frac{\partial (P_j - P_{ij})}{\partial P}\right)\\    &= \frac{\sum_{j=1}^n (P_j - P_{ij}) \frac{\partial (P_j - P_{ij})}{\partial P}}{\left( \sum_{j=1}^n \left ( x_j - P_{ij} \right )^2 \right)^{\frac{1}{2}}}\\    &= \frac{P - P_i}{\lVert P - P_i \lVert}\end{aligned}\label{gradientg} \tag{3}"](https://render.githubusercontent.com/render/math?math=%5cbegin%7baligned%7d%20%20%20%20%5cnabla%20g_i%28P%29%26%3d%20%5cnabla%20%5clVert%20P%20-%20P_i%20%5clVert%5c%5c%20%20%20%20%26%3d%20%5cnabla%20%5cleft%28%20%5csum_%7bj%3d1%7d%5en%20%5cleft%20%28%20P_j%20-%20P_%7bij%7d%20%5cright%20%29%5e2%20%5cright%29%5e%7b%5cfrac%7b1%7d%7b2%7d%7d%5c%5c%20%20%20%20%26%3d%20%5cfrac%7b1%7d%7b2%7d%20%5cleft%28%20%5csum_%7bj%3d1%7d%5en%20%5cleft%20%28%20P_j%20-%20P_%7bij%7d%20%5cright%20%29%5e2%20%5cright%29%5e%7b-%5cfrac%7b1%7d%7b2%7d%7d%20%5cleft%28%20%5csum_%7bj%3d1%7d%5en%202%28P_j%20-%20P_%7bij%7d%29%20%5cfrac%7b%5cpartial%20%28P_j%20-%20P_%7bij%7d%29%7d%7b%5cpartial%20P%7d%5cright%29%5c%5c%20%20%20%20%26%3d%20%5cfrac%7b%5csum_%7bj%3d1%7d%5en%20%28P_j%20-%20P_%7bij%7d%29%20%5cfrac%7b%5cpartial%20%28P_j%20-%20P_%7bij%7d%29%7d%7b%5cpartial%20P%7d%7d%7b%5cleft%28%20%5csum_%7bj%3d1%7d%5en%20%5cleft%20%28%20x_j%20-%20P_%7bij%7d%20%5cright%20%29%5e2%20%5cright%29%5e%7b%5cfrac%7b1%7d%7b2%7d%7d%7d%5c%5c%20%20%20%20%26%3d%20%5cfrac%7bP%20-%20P_i%7d%7b%5clVert%20P%20-%20P_i%20%5clVert%7d%5cend%7baligned%7d%5clabel%7bgradientg%7d%20%5ctag%7b3%7d)

Denklem \ref{gradientg} ile elde edilen eşitlik Denklem \ref{gradientfclosed} da yerine konularsa;

!["\begin{aligned}    \nabla f(P)&=\sum_{i \in S} \nabla g_i(P) g_i(P) - \sum_{i \in S}  d_i \nabla g_i(P) \\    &= \sum_{i \in S} \frac{P - P_i}{\lVert P - P_i \lVert} {\lVert P - P_i \lVert} - \sum_{i \in S}  d_i\frac{P - P_i}{\lVert P - P_i \lVert} \\    &= \sum_{i \in S} \left(P - P_i\right) - \sum_{i \in S}  d_i\frac{P - P_i}{\lVert P - P_i \lVert} \\    &= m P - \sum_{i \in S}  P_i - \sum_{i \in S}  d_i\frac{P - P_i}{\lVert P - P_i \lVert} \end{aligned}\label{gradientf} \tag{4}"](https://render.githubusercontent.com/render/math?math=%5cbegin%7baligned%7d%20%20%20%20%5cnabla%20f%28P%29%26%3d%5csum_%7bi%20%5cin%20S%7d%20%5cnabla%20g_i%28P%29%20g_i%28P%29%20-%20%5csum_%7bi%20%5cin%20S%7d%20%20d_i%20%5cnabla%20g_i%28P%29%20%5c%5c%20%20%20%20%26%3d%20%5csum_%7bi%20%5cin%20S%7d%20%5cfrac%7bP%20-%20P_i%7d%7b%5clVert%20P%20-%20P_i%20%5clVert%7d%20%7b%5clVert%20P%20-%20P_i%20%5clVert%7d%20-%20%5csum_%7bi%20%5cin%20S%7d%20%20d_i%5cfrac%7bP%20-%20P_i%7d%7b%5clVert%20P%20-%20P_i%20%5clVert%7d%20%5c%5c%20%20%20%20%26%3d%20%5csum_%7bi%20%5cin%20S%7d%20%5cleft%28P%20-%20P_i%5cright%29%20-%20%5csum_%7bi%20%5cin%20S%7d%20%20d_i%5cfrac%7bP%20-%20P_i%7d%7b%5clVert%20P%20-%20P_i%20%5clVert%7d%20%5c%5c%20%20%20%20%26%3d%20m%20P%20-%20%5csum_%7bi%20%5cin%20S%7d%20%20P_i%20-%20%5csum_%7bi%20%5cin%20S%7d%20%20d_i%5cfrac%7bP%20-%20P_i%7d%7b%5clVert%20P%20-%20P_i%20%5clVert%7d%20%5cend%7baligned%7d%5clabel%7bgradientf%7d%20%5ctag%7b4%7d)

bulunur. Burada !["m"](https://render.githubusercontent.com/render/math?math=m) verilen nokta sayısını (!["m=3"](https://render.githubusercontent.com/render/math?math=m%3d3)) göstermektedir. Bulunan !["\nabla f(P)"](https://render.githubusercontent.com/render/math?math=%5cnabla%20f%28P%29) ifadesi kullanılarak, !["\eta_k=\frac{1}{m}"](https://render.githubusercontent.com/render/math?math=%5ceta_k%3d%5cfrac%7b1%7d%7bm%7d) seçilen [En Dik İniş Yöntemi]({% post_url 2020-04-08-gradyan-yontemleri-ile-optimizasyon-optimization-using-gradient-methods %}) ile çözüm aşağıdaki şekilde hesaplanır.

!["\begin{aligned}P_{k+1} &= P_k - \eta_k \nabla f(P_k)\\&= P_k - \frac{1}{m} \left(  m P_k - \sum_{i \in S}  P_i - \sum_{i \in S}  d_i\frac{P_k - P_i}{\lVert P_k - P_i \lVert} \right)\\&= \frac{1}{m} \left( \sum_{i \in S}  P_i + \sum_{i \in S}  d_i\frac{P_k - P_i}{\lVert P_k - P_i \lVert} \right)\end{aligned}\label{optimalf} \tag{5}"](https://render.githubusercontent.com/render/math?math=%5cbegin%7baligned%7dP_%7bk%2b1%7d%20%26%3d%20P_k%20-%20%5ceta_k%20%5cnabla%20f%28P_k%29%5c%5c%26%3d%20P_k%20-%20%5cfrac%7b1%7d%7bm%7d%20%5cleft%28%20%20m%20P_k%20-%20%5csum_%7bi%20%5cin%20S%7d%20%20P_i%20-%20%5csum_%7bi%20%5cin%20S%7d%20%20d_i%5cfrac%7bP_k%20-%20P_i%7d%7b%5clVert%20P_k%20-%20P_i%20%5clVert%7d%20%5cright%29%5c%5c%26%3d%20%5cfrac%7b1%7d%7bm%7d%20%5cleft%28%20%5csum_%7bi%20%5cin%20S%7d%20%20P_i%20%2b%20%5csum_%7bi%20%5cin%20S%7d%20%20d_i%5cfrac%7bP_k%20-%20P_i%7d%7b%5clVert%20P_k%20-%20P_i%20%5clVert%7d%20%5cright%29%5cend%7baligned%7d%5clabel%7boptimalf%7d%20%5ctag%7b5%7d)

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
Yazılan kod parçası !["P_0=(0,0)"](https://render.githubusercontent.com/render/math?math=P_0%3d%280%2c0%29) ve !["P_0=(10,10)"](https://render.githubusercontent.com/render/math?math=P_0%3d%2810%2c10%29) gibi farklı iki başlangıç noktasından, elde edilen yeni konum !["P_{k+1}"](https://render.githubusercontent.com/render/math?math=P_%7bk%2b1%7d) ile eski konum !["P_k"](https://render.githubusercontent.com/render/math?math=P_k) arasındaki fark !["10^{-3}"](https://render.githubusercontent.com/render/math?math=10%5e%7b-3%7d) ten küçük olana kadar çalıştırıldığında, toplam !["17"](https://render.githubusercontent.com/render/math?math=17) adımda aşağıdaki görselde verilen adımları izleyerek !["P_x=(4.24, 3.20)"](https://render.githubusercontent.com/render/math?math=P_x%3d%284.24%2c%203.20%29) noktasına ulaşmaktadır.

|-----------|-----------|
![kaynak konumlandırma örnek][source_localization_solution1] | ![kaynak konumlandırma örnek][source_localization_solution2]

Verilen grafiklerde, arka plan renkleri ve kontur çizgileri !["P=(x,y)"](https://render.githubusercontent.com/render/math?math=P%3d%28x%2cy%29) seçilmesi durumunda elde edilecek hatayı göstermektedir. Siyah ile işaretlenen nokta iterasyonun başlangıç noktasını, kırmızı nokta ise iterasyonlar sonucunda ulaşılan noktayı göstermektedir. Turuncu ile gösterilen noktalar her iterasyon sonucunda gidilen yeni noktayı göstermektedir.

**Referanslar**
* Beck, Amir. Introduction to nonlinear optimization: Theory, algorithms, and applications with MATLAB. Vol. 19. Siam, 2014.

[RESOURCES]: # (List of the resources used by the blog post)
[source_localization_example]: /assets/post_resources/source_localization/source_localization_example.svg
[source_localization_solution1]: /assets/post_resources/source_localization/source_localization_solution1.png
[source_localization_solution2]: /assets/post_resources/source_localization/source_localization_solution2.png