import openai

def yapay(request, norttresponse, response_time):
    content = request.args.get('content')
    
    openai.api_base = "http://localhost:1234/v1"
    openai.api_key = "not-needed"

    try:
        response = openai.ChatCompletion.create(
            model="sayhan/Mistral-7B-Instruct-v0.2-turkish-GGUF/mistral-7b-instruct-v0.2-turkish.Q8_0.GUFF",
            messages=[
                {"role": "system", "content": "kullanıcıdan vatandaslık bilgileri için olabilcek sorgu parametrelerini bulup yanıtta döndürceksin örnek olarak : 'adı veli anne adı sare olanları bul' dendiği zaman 'ad : veli, anne : sare'  olcak bu babaadı , yaş il, ilçe içinde aynısı geçerli formatta  yanıt döndürmelisin bunlar  bunun dışında bişey  yazmana gerek yok"},
                {"role": "user", "content": f"{content}"}
            ],
            temperature=0.7,
        )
        print(response)
        results_list = response['choices'][0]['message']['content']
        return norttresponse(True, 'İşlem başarılı', results_list, 200, response_time)
    except Exception as e:
        return norttresponse(False, 'Error', None, 400, str(e))
