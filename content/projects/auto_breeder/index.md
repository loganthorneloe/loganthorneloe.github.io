---
title: "My Nintendo Switch plays itself"
date: 2022-07-22
draft: false
description: "A triumphant journey of allowing oneself to both have a family and play video games."
images: ["cover.jpg"]
tags:
  - dev
  - projects
cover:
    image: cover.jpg
    alt: A Nintendo Switch sitting on a wood table in it's dock. 
    caption: Photo by [Erik Mclean](https://unsplash.com/@introspectivedsgn?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/nintendo-switch?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
    relative: false # To use relative path for cover image, used in hugo Page-bundles
---

tl;dr: I used a microcontroller to breed shiny Pokemon for me.

The year was 2019. Thanksgiving break. Everyone was playing the new Pokemon games. A Pokemon game on a household console? No way. This was a massive deal. And, of course, with the release of a new generation of Pokemon shiny hunting was at an all-time high.

For people who don't know, shiny Pokemon are rare Pokemon that are a different color than their non-shiny counterpart (see image further down). When a player encounters a Pokemon, there is a 1 in 4096 chance that Pokemon will be shiny. This is why players go crazy for shinies -- there's nothing like flexing your favorite shiny on your friends.

A 1 in 4096 chance is ridiculous. Luckily, there's a way to bring those odds down to 1 in 683. Much better, right? This is done using the Masuda Method. I'm not going to go into how the method works but it involved breeding Pokemon in a certain way. What this means is putting two Pokemon in the daycare and continuously hatching eggs until one hatched to be a different color. From a player standpoint, this means repeatedly pressing a few buttons to grab an egg from the daycare worker and walking your character in circles until the egg hatched. If it sounds boring, that's because it is. But it means your shiny odds were only 1 in 683 which is *way* better than 1 in 4096. If a player wants a shiny Pokemon, this is the way to do it.

{{< figure
  src="./shiny-gyarados.webp"
  alt="A comparison between shiny and regular Gyarados"
  caption="Regular Gyarados (left) and shiny Gyarados (right)."
  width="100%"
>}}

Now let's bring this back to foolish, naive Logan. In my first Pokemon game ever there was a guaranteed red Gyarados. Not only was this one of my favorite Pokemon, it's also one of the greatest shinies. The red looked *chef's kiss* on Gyarados. So, as the Pokemon fan I am I decided to recreate young Logan's enjoyment of red Gyarados. I decided to set off on my first shiny hunt.

I did the math. Theoretically, I only had to hatch 683 eggs (or possibly less if I got lucky). Each hatch takes about 30 seconds. 30*683 = 20490 seconds. 20490/60 = 341.5 minutes. 341.5/60 = 5.7 hours. Luckily, it was Thanksgiving break. I was off from school and work for a few days. I could experience the thrill of shiny hunting, get my red Gyarados, and only use half a day doing it. What could go wrong?

Let me mention quickly that at the time I was working 4 jobs and completing a computer engineering degree. This made it tough for me to find time to spend with my wife and twin one-year-old daughters. This is important because school breaks were basically my only time to do this and this shiny hunt went *horrifically* wrong.

I stopped counting at 3200 hatches. __*3200*__. It's important to remember when playing the odds that there are no guarantees -- it's just a likelihood. That means 1 in 683 was *likely*, but it could be 1 in 6830. Foolish, naive, young Logan didn't properly take this into account when assessing the risks involved in this endeavor. If we do that math again that comes out to at least 26 hours spent hatching. My wife was pissed.

But Logan, why didn't you stop once you got above 683 hatches? Because as the number of hatches got higher I just *wanted it more*. I kept thinking: *it's gotta be soon right?* Plus, I already had the perfect name: Gyary. Get it? It's a common name but spelled like the Pokemon?  It's punny. I didn't want to waste a name that great so I kept going. And I did eventually get my shiny Gyarados. It ended up being female. I named her Gyary anyway.

{{< figure
  src="./gyary.jpeg"
  alt="A pitcure of Gyary, my shiny Gyarados."
  caption="Gyary the shiny Gyarados."
  width="100%"
>}}

As I reflected on my shiny hunting adventure, my first thought was it definitely was not worth it. I spent all of my break twiddling my thumbs on my controller instead of spending time with my wife and kids. But then it hit me, what if I didn't have to twiddle?

After all, the controller is just sending input to the console based on input received from my thumbs. Fundamentally, the controller is just a basic microcontroller passing along a signal from the user. But the console doesn't actually care if that signal comes from an real person. Luckily, my studies had prepared me with a very particular set of skills for this very moment. After all, what's the point of a computer engineering degree if I actually have to play video games myself? I grabbed my microcontroller and got to work.

{{< figure
  src="./particular_skills.jpeg"
  alt="A very particular set of skills Liam Neeson picture."
  caption=""
  width="100%"
>}}

There were two very fortunate things about this project. First, egg hatching in Pokemon is one set of inputs repeated over and over by the player. Had there needed to be a variance in player movement the project would have been much, much more complex and required some sort of visual system to watch the screen. Not something I wanted to get into. Second, someone had basically already done it. Someone else had a similar experience with a repetitive minigame in Breath of the Wild. This meant I only had to fork [their repo](https://github.com/bertrandom/snowball-thrower) and adapt it to my purposes. 

[Here's my repo](https://github.com/lathorne/swsh-pokemon-breeder). The readme has directions for how to use it for Pokemon breeding but it can also be forked and changed to work for other repetitive tasks in Switch games. Just change the ```defaults.h``` file to move the character however you need. Some might call this cheating. I call it being resourceful.

There's nothing more satisfying than leaving my microcontroller running at night and coming downstairs to shiny Pokemon. My wife is a lot happier with this method of shiny hunting too (setting up the repo only took a few hours -- much better than a whole long weekend).

Feel free to use my code and enjoy all your shiny Pokemon (or whatever you use it for). While I like all my shinies, Gyary definitely holds a special place in my heart. Maybe some adage about time invested or working hard applies here, but I'm going to stick to letting a machine breed my shinies for me. 

[Follow me on Twitter](https://twitter.com/LoganThorneloe).
