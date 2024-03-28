import re
import urllib.parse

url = 'https://www.amazon.com/sspa/click?ie=UTF8&spc=MTo2Mjk2MDY0NTc3MDY0MDg3OjE3MTE2MjQyMTI6c3BfYXRmOjMwMDAzMTY0Nzg2NzQwMjo6MDo6&url=%2FDinosaur-Storage-Educational-Realistic-Jurassic%2Fdp%2FB0B3RRZX8R%2Fref%3Dsr_1_1_sspa%3Fcrid%3D3LW1ZP5WWO90O%26dib%3DeyJ2IjoiMSJ9.BjmsOYJgHEQNsFiP4j-_v_9aBCEjvuLgJwlX3rnODb62Xzuc4RmxCwrDp9S1VoXG9qPqo3WmRUhACYe50Lj_1yVR7PS99m6YGw3kP8G15LnsnxFHDAc2AgzYqezcdD9-u-sQ5YNTwv_hFdOuEheuNGKPpC8Rk4W13IjGByP5fjNE0xzjmZTQHPh9B47b1wiXJBP9mGGyYzfGfyapWsudJ7v1ka4hQMxRXD6fIf3ebPvWbuXrr_E_qPRIdFhDwjZkfII4zILCPs-7cs2QvcFD3u88HnpgI6LFfGNnlXFrvpg.tSVgjVHfPgnLLyoxZtaiXK0Ickl50rGxz8C9inLB8iA%26dib_tag%3Dse%26keywords%3Ddinosaur%2Btoys%26qid%3D1711624212%26sprefix%3Ddinosaurtoy%2Bs%252Caps%252C319%26sr%3D8-1-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGY%26psc%3D1'

new_url, asin, country = None, None, None
if 'sspa' in url:
    asin_pattern = re.compile(r'dp%2F([A-Za-z0-9]{10})')
else:
    asin_pattern = re.compile(r'/dp/([A-Z0-9]{10})')
match = asin_pattern.search(url)
asin = match[1] if match else None

parsed_url = urllib.parse.urlparse(url)
domain = parsed_url.netloc
domain_parts = domain.split('.')
if len(domain_parts) >= 4:
    domain_suffix = f'{domain_parts[-2]}.{domain_parts[-1]}'
else:
    domain_suffix = domain_parts[-1]
domain_suffix_country_dict = {'com': 'us', 'co.uk': 'uk'}
country = domain_suffix_country_dict.get(domain_suffix, domain_suffix)

print(domain_suffix)

#domain_suffix_country_dict = {'com': 'us', 'co.uk': 'uk'}
#domain_suffix = re.search('amazon\\.([a-zA-Z.]+)', url)
#if domain_suffix:
#    domain_suffix = domain_suffix[1]
#country = domain_suffix_country_dict.get(domain_suffix, domain_suffix)

new_url = f'https://www.amazon.com/dp/{asin}'
print(new_url, asin, country) 


# 编译正则表达式提取ASIN
asin_pattern = re.compile(r'/dp/([A-Z0-9]{10})')
match = asin_pattern.search(url)
asin = match[1] if match else None
country = url.split('/')[2].split('.')[-1]
if country == 'com':
    Country = 'us'

print()