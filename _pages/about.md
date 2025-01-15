---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% if site.google_scholar_stats_use_cdn %}
{% assign gsDataBaseUrl = "https://cdn.jsdelivr.net/gh/" | append: site.repository | append: "@" %}
{% else %}
{% assign gsDataBaseUrl = "https://raw.githubusercontent.com/" | append: site.repository | append: "/" %}
{% endif %}
{% assign url = gsDataBaseUrl | append: "google-scholar-stats/gs_data_shieldsio.json" %}

<span class='anchor' id='about-me'></span>

I am Cheng Yang, currently an associate professor from Beijing University of Posts and Telecommunications. Before that, I got B.S. and Ph.D. degrees from Tsinghua University at 2014 and 2019, respectively. My research interest includes graph neural networks, large language models, network embedding, recommender systems, etc. I have published more than 50 top journal and conference papers, and gained <a href='https://scholar.google.com/citations?user=OlLjVUcAAAAJ'><img src="https://img.shields.io/endpoint?url={{ url | url_encode }}&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a> citations as shown by [Google Scholar](https://scholar.google.com/citations?user=OlLjVUcAAAAJ). He was named by Baidu as one of the Top 100 Chinese Young Scholars in Artificial Intelligence, and also supported by the Young Talent Support Project of CAST.

# 🔥 News
- *2024.12*: &nbsp;🎉🎉 吴文俊人工智能科学技术奖 (青年科技奖). 
- *2024.12*: &nbsp;🎉🎉 3 papers are accepted by AAAI 2025.

# 🏫 Work Experience
- *2021.12 - Present*, Associate Professor, School of Computer Sciences, Beijing University of Posts and Telecommunications, Beijing, China
- *2019.07 - 2021.12*, Lecturer, School of Computer Sciences, Beijing University of Posts and Telecommunications, Beijing, China

# 📝 Publications

## 🔖 Selected Publications

- <span class="conference-badge">arxiv preprint</span> 
[GraphTeam: Facilitating Large Language Model-based Graph Analysis via Multi-Agent Collaboration](https://arxiv.org/abs/2410.18032)
Xin Li\*, Qizhi Chu\*, Yubin Chen\*, Yang Liu, Yaoqi Liu, Zekai Yu, Weize Chen, Chen Qian, Chuan Shi, **Cheng Yang<sup>†</sup>**
[![](https://img.shields.io/badge/Source Code-ffffff?logo=github&style=social)](https://github.com/BUPT-GAMMA/GraphTeam)
<!-- [![](https://img.shields.io/github/stars/BUPT-GAMMA/GraphTeam?style=social&label=Code+Stars)](https://github.com/BUPT-GAMMA/GraphTeam) -->
<a href='https://scholar.google.com/citations?view_op=view_citation&hl=zh-CN&user=OlLjVUcAAAAJ&citation_for_view=OlLjVUcAAAAJ:Mojj43d5GZwC'><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Falbertyang33%2Falbertyang33.github.io%2Fgoogle-scholar-stats%2Fselected_pubs%2FMojj43d5GZwC.json&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a>. \
[**Demo**](http://graphteam.cloud/gt/): **You can play it, enjoy yourself!**

- <span class="conference-badge">NeurIPS 2024</span>
[(ProGraph) Can Large Language Models Analyze Graphs like Professionals? A Benchmark, Datasets and Models](https://arxiv.org/abs/2409.19667)
Xin Li\*, Weize Chen\*, Qizhi Chu, Haopeng Li, Zhaojun Sun, Ran Li, Chen Qian, Yiwei Wei, Zhiyuan Liu, Chuan Shi, Maosong Sun, **Cheng Yang<sup>†</sup>**
<!-- [**Source Code**](https://github.com/BUPT-GAMMA/ProGraph) -->
[**Models and Datasets**](https://huggingface.co/lixin4sky/ProGraph)
[![](https://img.shields.io/badge/Source Code-ffffff?logo=github&style=social)](https://github.com/BUPT-GAMMA/ProGraph)
<a href='https://scholar.google.com/citations?view_op=view_citation&hl=zh-CN&user=OlLjVUcAAAAJ&citation_for_view=OlLjVUcAAAAJ:t6usbXjVLHcC'><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Falbertyang33%2Falbertyang33.github.io%2Fgoogle-scholar-stats%2Fselected_pubs%2Ft6usbXjVLHcC.json&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a>.

- <span class="conference-badge">ICLR 2024</span>
[AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors](https://arxiv.org/abs/2308.10848)
Weize Chen\*, Yusheng Su\*, Jingwei Zuo, **Cheng Yang<sup>†</sup>**, Chenfei Yuan, Chi-Min Chan, Heyang Yu, Yaxi Lu, Yi-Hsin Hung, Chen Qian, Yujia Qin, Xin Cong, Ruobing Xie, Zhiyuan Liu<sup>†</sup>, Maosong Sun, Jie Zhou
<!-- [**Source Code**](https://github.com/OpenBMB/AgentVerse) -->
[![](https://img.shields.io/badge/Source Code-ffffff?logo=github&style=social)](https://github.com/OpenBMB/AgentVerse)
<!-- <strong><span class='show_paper_citations' data='OlLjVUcAAAAJ:8AbLer7MMksC'></span></strong> -->
<a href='https://scholar.google.com/citations?view_op=view_citation&hl=zh-CN&user=OlLjVUcAAAAJ&citation_for_view=OlLjVUcAAAAJ:8AbLer7MMksC'><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Falbertyang33%2Falbertyang33.github.io%2Fgoogle-scholar-stats%2Fselected_pubs%2F8AbLer7MMksC.json&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a>.

- <span class="conference-badge">WWW 2024</span>
[GraphTranslator: Aligning Graph Model to Large Language Model for Open-ended Tasks](https://arxiv.org/abs/2402.07197)
Mengmei Zhang, Mingwei Sun, Peng Wang, Shen Fan, Yanhu Mo, Xiaoxiao Xu, Hong Liu, **Cheng Yang<sup>†</sup>**, Chuan Shi<sup>†</sup>
<!-- [**Source Code**](https://github.com/alibaba/GraphTranslator) -->
[![](https://img.shields.io/badge/Source Code-ffffff?logo=github&style=social)](https://github.com/alibaba/GraphTranslator)
<!-- <strong><span class='show_paper_citations' data='OlLjVUcAAAAJ:sSrBHYA8nusC'></span></strong> -->
<a href='https://scholar.google.com/citations?view_op=view_citation&hl=zh-CN&user=OlLjVUcAAAAJ&citation_for_view=OlLjVUcAAAAJ:sSrBHYA8nusC'><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Falbertyang33%2Falbertyang33.github.io%2Fgoogle-scholar-stats%2Fselected_pubs%2FsSrBHYA8nusC.json&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a>.

- <span class="conference-badge">arXiv preprint</span>
[Towards Graph Foundation Models: A Survey and Beyond](https://arxiv.org/abs/2310.11829)
Jiawei Liu\*, **Cheng Yang\***, Zhiyuan Lu, Junze Chen, Yibo Li, Mengmei Zhang, Ting Bai, Yuan Fang, Lichao Sun, Philip S. Yu, Chuan Shi
<!-- [**Source Code**](https://github.com/alibaba/GraphTranslator) -->
<!-- [![](https://img.shields.io/badge/Source Code-ffffff?logo=github&style=social)](https://github.com/alibaba/GraphTranslator) -->
<!-- <strong><span class='show_paper_citations' data='OlLjVUcAAAAJ:sSrBHYA8nusC'></span></strong> -->
<a href='https://scholar.google.com/citations?view_op=view_citation&hl=zh-CN&user=OlLjVUcAAAAJ&citation_for_view=OlLjVUcAAAAJ:vRqMK49ujn8C'><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Falbertyang33%2Falbertyang33.github.io%2Fgoogle-scholar-stats%2Fselected_pubs%2FvRqMK49ujn8C.json&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a>.

- <span class="conference-badge">arXiv preprint</span>
[Data-centric Graph Learning: A Survey](https://arxiv.org/abs/2310.04987)
Yuxin Guo\*, Deyu Bo\*, **Cheng Yang<sup>†</sup>**, Zhiyuan Lu, Zhongjian Zhang, Jixi Liu,Yufei Peng, Chuan Shi<sup>†</sup>
<!-- [**Source Code**](https://github.com/alibaba/GraphTranslator) -->
<!-- [![](https://img.shields.io/badge/Source Code-ffffff?logo=github&style=social)](https://github.com/alibaba/GraphTranslator) -->
<!-- <strong><span class='show_paper_citations' data='OlLjVUcAAAAJ:sSrBHYA8nusC'></span></strong> -->
<a href='https://scholar.google.com/citations?view_op=view_citation&hl=zh-CN&user=OlLjVUcAAAAJ&citation_for_view=OlLjVUcAAAAJ:AXPGKjj_ei8C'><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Falbertyang33%2Falbertyang33.github.io%2Fgoogle-scholar-stats%2Fselected_pubs%2FAXPGKjj_ei8C.json&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a>.

- <span class="conference-badge">WWW 2021</span>
[(CPF) Extract the Knowledge of Graph Neural Networks and Go Beyond it: An Effective Knowledge Distillation Framework](https://arxiv.org/abs/2103.02885)
**Cheng Yang**, Jiawei Liu, Chuan Shi<sup>†</sup>
<!-- [**Source Code**](https://github.com/thunlp/JNTM) -->
[![](https://img.shields.io/badge/Source Code-ffffff?logo=github&style=social)](https://github.com/BUPT-GAMMA/CPF)
<!-- <strong><span class='show_paper_citations' data='OlLjVUcAAAAJ:e5wmG9Sq2KIC'></span></strong> -->
<a href='https://scholar.google.com/citations?view_op=view_citation&hl=zh-CN&user=OlLjVUcAAAAJ&citation_for_view=OlLjVUcAAAAJ:e5wmG9Sq2KIC'><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Falbertyang33%2Falbertyang33.github.io%2Fgoogle-scholar-stats%2Fselected_pubs%2Fe5wmG9Sq2KIC.json&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a>.

- <span class="conference-badge">KDD 2020</span>
[(AGE) Adaptive Graph Encoder for Attributed Graph Embedding](https://arxiv.org/abs/2007.01594)
Ganqu Cui, Jie Zhou, **Cheng Yang<sup>†</sup>**, Zhiyuan Liu<sup>†</sup>
<!-- [**Source Code**](https://github.com/thunlp/AGE) -->
[![](https://img.shields.io/badge/Source Code-ffffff?logo=github&style=social)](https://github.com/thunlp/AGE)
<!-- <strong><span class='show_paper_citations' data='OlLjVUcAAAAJ:-f6ydRqryjwC'></span></strong> -->
<a href='https://scholar.google.com/citations?view_op=view_citation&hl=zh-CN&user=OlLjVUcAAAAJ&citation_for_view=OlLjVUcAAAAJ:-f6ydRqryjwC'><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Falbertyang33%2Falbertyang33.github.io%2Fgoogle-scholar-stats%2Fselected_pubs%2F-f6ydRqryjwC.json&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a>.

- <span class="conference-badge">TOIS 2017</span>
[(JNTM) A Neural Network Approach to Jointly Modeling Social Networks and Mobile Trajectories](https://arxiv.org/abs/1606.08154)
**Cheng Yang**, Maosong Sun, Wayne Xin Zhao<sup>†</sup>, Zhiyuan Liu<sup>†</sup>, Edward Y.Chang
<!-- [**Source Code**](https://github.com/thunlp/JNTM) -->
[![](https://img.shields.io/badge/Source Code-ffffff?logo=github&style=social
)](https://github.com/thunlp/JNTM)
<!-- <strong><span class='show_paper_citations' data='OlLjVUcAAAAJ:qjMakFHDy7sC'></span></strong> -->
<a href='https://scholar.google.com/citations?view_op=view_citation&hl=zh-CN&user=OlLjVUcAAAAJ&citation_for_view=OlLjVUcAAAAJ:qjMakFHDy7sC'><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Falbertyang33%2Falbertyang33.github.io%2Fgoogle-scholar-stats%2Fselected_pubs%2FqjMakFHDy7sC.json&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a>.

- <span class="conference-badge">IJCAI 2015</span>
[(TADW) Network Representation Learning with Rich Text Information](https://nlp.csai.tsinghua.edu.cn/~yangcheng/publications/ijcai15.pdf)
Cheng Yang, Zhiyuan Liu<sup>†</sup>, Deli Zhao, Maosong Sun, Edward Y. Chang
<!-- [**Source Code**](https://github.com/benedekrozemberczki/TADW) -->
<!-- [![](https://img.shields.io/badge/Source Code-ffffff?logo=github&style=social)](https://github.com/benedekrozemberczki/TADW) -->
<!-- <strong><span class='show_paper_citations' data='OlLjVUcAAAAJ:u5HHmVD_uO8C'></span></strong> -->
<a href='https://scholar.google.com/citations?view_op=view_citation&hl=zh-CN&user=OlLjVUcAAAAJ&citation_for_view=OlLjVUcAAAAJ:u5HHmVD_uO8C'><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Falbertyang33%2Falbertyang33.github.io%2Fgoogle-scholar-stats%2Fselected_pubs%2Fu5HHmVD_uO8C.json&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a>.

<!-- ## ⌛️ 2024 -->



# 🎖 Honors and Awards

- *2024* World's **Top 2%** Scientists by Stanford/Elsevier.
- *2023* Young Talent Support Project of CAST (青托计划).
- *2022* Top 100 Chinese Young Scholars in Artificial Intelligence (Baidu)
- *2022* World Internet Conference Awards for Pioneering Science and Technology. Systematized Basic Algorithms and Open-Source Tools for Representation Learning of Large Scale Knowledge Graph (**ranking 4th**)
- *2020* First Prize of the State Natural Science Award, and the Outstanding Achievement Awards for Scientific Research in Institutes of Higher Education (Science and Technology) by the Ministry of Education. A Representation Learning Method for Structured Knowledge (**ranking 4th**)
- *2020* Outstanding Doctoral Dissertation Award (Chinese Information Processing Society of China) (中文信息学会优秀博士学位论文奖)
- *2019* Hotspot Paper Award of SCIENTIA SINICA Informationis (Network representation learning: an overview)
- *2019* **Outstanding Graduate Award** (Department of Computer Science and Technology, Tsinghua University) (清华大学优秀毕业生)

# 📖 Educations
- *2014.08 - 2019.07*, Department of Computer Science and Technology, Tsinghua University Aug. 2014 - Jul. 2019, PhD, Advisor: Prof. Maosong Sun.

- *2010.08 - 2014.07*, Institute for Interdisciplinary Information Sciences (Computer Science Pilot Class), Tsinghua University Aug. 2010 - Jul. 2014, B.S.

<!-- Department of Computer Science and Technology, Tsinghua University Aug. 2014 - Jul. 2019, PhD, Advisor: Prof. Maosong Sun -->

<!-- Institute for Interdisciplinary Information Sciences (Computer Science Pilot Class), Tsinghua University Aug. 2010 - Jul. 2014, B.S. -->

# 💬 Invited Talks
- *2024*, WWW24 Tutorial: Towards Graph Foundation Models [Link](https://www2024.thewebconf.org/program/tutorials/) [Part I](../talks/WWW24Tutorial_GFM_Part1.pdf) [Part II](../talks/WWW24Tutorial_GFM_Part2.pdf) [Part III](../talks/WWW24Tutorial_GFM_Part3.pdf).
- *2024*, IJCAI 2024 LKM workshop [Link](https://lkm2024.openkg.org/) [PDF](../talks/Towards%20Graph%20Foundation%20Models-Cheng%20Yang.pdf)

<!-- # 💻 Internships
- *2019.05 - 2020.02*, [Lorem](https://github.com/), China. -->