Use the below .tex file as a starter template.

```
\documentclass[twocolumn]{article}
\usepackage[T1]{fontenc}
\usepackage{kpfonts}

\usepackage{geometry}
%\geometry{margin=1.0in}

\usepackage[square, numbers]{natbib}
\bibliographystyle{abbrvnat}

\usepackage{xcolor}
\definecolor{unicolor}{HTML}{990000}
\usepackage[hidelinks]{hyperref}
\hypersetup{
   colorlinks=true,
   linkcolor=blue,
   filecolor=black,
   citecolor=unicolor,
   urlcolor=blue
}

\usepackage{amssymb}
\usepackage{amsmath}

\linespread{1.0}

\usepackage{authblk}
\author[1,$\dagger$]{Author 1}
\author[2]{Author 2}
\author[3]{Author 3}

\affil[1]{Affiliation 1}
\affil[2]{Affiliation 2}
\affil[3]{Affiliation 3}
\affil[$\dagger$]{\footnotesize Corresponding author: \texttt{youremail@uni.edu}}
\date{}

\title{[Paper Title]}

\begin{document}
\maketitle

% Sections will be inserted here

\bibliography{main.bib}
\end{document}
```
