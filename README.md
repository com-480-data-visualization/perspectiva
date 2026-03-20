# Project of Data Visualization (COM-480)

| Student's name | SCIPER |
| -------------- | ------ |
| Andrine Hjerto | 423210 |
| Vinayak Joshi | 423333 |
| Gaspar Benavente | 421992 |

[Milestone 1](#milestone-1) • [Milestone 2](#milestone-2) • [Milestone 3](#milestone-3)

## Milestone 1 (20th March, 5pm)

**10% of the final grade**

### Dataset

> Find a dataset (or multiple) that you will explore. Assess the quality of the data it contains and how much preprocessing / data-cleaning it will require before tackling visualization. We recommend using a standard dataset as this course is not about scraping nor data processing.
>
> Hint: some good pointers for finding quality publicly available datasets ([Google dataset search](https://datasetsearch.research.google.com/), [Kaggle](https://www.kaggle.com/datasets), [OpenSwissData](https://opendata.swiss/en/), [SNAP](https://snap.stanford.edu/data/) and [FiveThirtyEight](https://data.fivethirtyeight.com/)).

### Problematic

> Frame the general topic of your visualization and the main axis that you want to develop.
> - What am I trying to show with my visualization?
> - Think of an overview for the project, your motivation, and the target audience.

Motivation
This visualization is grounded in the idea that the version of reality that news media constructs is never neutral, and rarely universal. The world is interconnected, but the news is localized, filtered and shaped by economic interests, political alliances, history, and perceived consequences of events. This leaves people with fundamentally different understandings of the same reality. This visualization makes those differences visible.

Main Goal & Overview
Our visualization explores how specific events and topics are reported, covered, and framed differently across the world and over time. Based on the GDELT dataset, an archive of online newspaper data, and AI sentiment analysis, it surfaces how the same moments in history have been portrayed differently depending on location, and how these portrayals have changed through time.

The visualization affords users to explore quantitative data on a 3D world map, across dimensions such as place, time, sentiment, and sub-themes, and to compare coverage across countries. In addition, we will add complimentary 2D views for information that is better communicated in charts, graphs, networks, etc. It also allows users to gain qualitative insight, by linking directly to the source articles that the data is based on.

As a starting point, the visualization will focus on three topics: Vaccines, Stock Market, and Social Media. These are chosen for their global relevance, and the different ways they have been covered across countries and over time. For future extension, interesting themes might include wars, political views, climate change. 

Target Audience 
The target audience falls into two groups: the curious learner and the deep researcher. The curious learners are people who want to explore global trends and gain an intuitive and visually engaging insight of how events are covered around the world. The deep researcher can use the visualization to filter, compare and extract data for their own analysis. 


### Exploratory Data Analysis

> Pre-processing of the data set you chose
> - Show some basic statistics and get insights about the data

### Related Work

**Existing approaches.** The GDELT Project (blog.gdeltproject.org) publishes extensive
research on their own dataset — conflict monitoring, election analysis, pandemic
tracking — but outputs are static snapshots aimed at researchers, not interactive
public tools. Media Cloud (mediacloud.org) tracks global media attention across
thousands of outlets and supports country-level comparisons over time, but has no
sentiment layer and no geographic animation. Newsmap (newsmap.ijmacd.com) visualizes
Google News as a live treemap by country, capturing news distribution in real time but
with no time dimension and no topic tracking.

**Our originality.** Our approach is centered around the dynamic visualization over time.
The objective is to combine how data spreads from source, how sentiment changes over time,
and how specific major events could drastically change this. We track these
dimensions simultaneously for user-defined topics — to our knowledge no public tool
does this.

**Visual inspiration.** Chronotrains (chronotrains.com) shows rail reachability
spreading outward from a city as a time slider advances — the interaction model we
adapt for news diffusion. The Reuters COVID tracker demonstrated that epidemiological
and narrative spread share the same visual grammar: a phenomenon rippling outward
across a world map over weeks. The Pudding (pudding.cool) influenced our scrollytelling
approach — guiding users through annotated event stops rather than presenting a raw
dashboard.

## Milestone 2 (17th April, 5pm)

**10% of the final grade**


## Milestone 3 (29th May, 5pm)

**80% of the final grade**


## Late policy

- < 24h: 80% of the grade for the milestone
- < 48h: 70% of the grade for the milestone

