# Auto_coding

[![CI](https://github.com/pzy2000/Auto_coding/actions/workflows/main.yml/badge.svg)](https://github.com/pzy2000/Auto_coding/actions/workflows/main.yml)[![DeepSource](https://deepsource.io/gh/pzy2000/Auto_coding.svg/?label=resolved+issues&show_trend=true&token=JmxpqvGwzeIt7g-Y8GZMWyWi)](https://deepsource.io/gh/pzy2000/Auto_coding/?ref=repository-badge)
<p align="left">
  <a href="https://raw.githubusercontent.com/nonebot/nonebot2/master/LICENSE">
    <img src="https://img.shields.io/github/license/nonebot/nonebot2" alt="license">
  </a>
</p>
<p align="center">
    <a href="https://github.com/badges/shields/graphs/contributors" alt="Contributors">
        <img src="https://img.shields.io/github/contributors/badges/shields" /></a>
    <a href="#backers" alt="Backers on Open Collective">
        <img src="https://img.shields.io/opencollective/backers/shields" /></a>
    <a href="#sponsors" alt="Sponsors on Open Collective">
        <img src="https://img.shields.io/opencollective/sponsors/shields" /></a>
    <a href="https://github.com/badges/shields/pulse" alt="Activity">
        <img src="https://img.shields.io/github/commit-activity/m/badges/shields" /></a>
    <a href="https://coveralls.io/github/badges/shields">
        <img src="https://img.shields.io/coveralls/github/badges/shields"
            alt="coverage"></a>
    <a href="https://lgtm.com/projects/g/badges/shields/alerts/">
        <img src="https://img.shields.io/lgtm/alerts/g/badges/shields"
            alt="Total alerts"/></a>
    <a href="https://discord.gg/MdgTD4v6">
        <img src="https://img.shields.io/discord/308323056592486420?logo=discord"
            alt="chat on Discord"></a>
    <a href="https://twitter.com/intent/follow?screen_name=pzy2000">
        <img src="https://img.shields.io/twitter/follow/pzy2000?style=social&logo=twitter"
            alt="follow on Twitter"></a>
</p>

An auto coding tool for python,off-brand github-copliot,trained by GPT2 transformer,fed with github public repos codes

It contains a GPT2 model trained from scratch (not fine tuned) on Python code from Github. Overall, it was ~80GB of pure Python code, the current model is a mere 2 epochs through this data, so it may benefit greatly from continued training and/or fine-tuning.

Input to the model is code, up to the context length of 1024.

# ?????????
<p align="center">
  <a>
    <img src="https://raw.githubusercontent.com/pzy2000/Auto_coding/qt/album/gpt-cpp.png">
  </a>
</p>

# ????????????

?????????????????????????????????????????????????????????????????????????????????test.py(??????????????????)!

???????????????????????????????????????????????????????????????????????????

# ??????
??????????????????????????????????????????7.use_model.py???test.py??????????????????coding????????????

????????????:https://huggingface.co/Sentdex/GPyT/blob/main/pytorch_model.bin

# ??????
test.py?????????????????????????????????????????????keyboard.txt???use_model.py????????????txt?????????????????????????????????????????????????????????

# Here's a quick example of using this model:
```c++
    #include<iostream>
```
# Should produce:
```c++
    #include<iostream>
    using namespace std;
    
    int main() {
```
