# Metaphoric ... in Git.

After a while of having Metaphoric lay dormant (the last thing I posted was back in 2011), I started thinking about
what I could improve in order for me to actually start using it. It's not that I don't have anything to write about;
actually I run into plenty of interesting stuff during an average day. I built the lastI Metaphoric when I was really
into making everything dynamic and using [CakePHP](http://www.cakephp.org) on a daily basis, so it used Cake backed up
by the Croogo CMS (as I was too lazy to write the functionality myself). Turns out this was an unfortunate choice,
because while I'm not too lazy to write blog posts, I actually _am_ too lazy to maintain the blog software itself.
After a while the Cake version got outdated, Croogo got outdated and everything got terribly slow.
So I sat down and looked at the things I thought would be important for my new blog:

- Low content-creation treshold. When I was writing blog posts I often found myself typing its content in a text editor,
  only to copy it over to the CMS later and save it; obviously repeating the process when I was making a change. Saving
  changes was slow, adding files was a pain, markup was a pain... actually everything about the content creation process
  was a pain. This needed to change.
- Modified layout. The last one was actually a little too fancy, and didn't focus too much on what a blog should focus
  on: reading. Didn't want to spend too much effort here; just take some parts of the existing layout and make it simpler
  and more reading-friendly.
- Static content. I don't care much about having everything dynamic anymore; blog content after all is simply
  static content; so that's the way it should be presented.

I started [MetaphoricJS](http://github.com/ElteHupkes/MetaphoricJS) a while ago to play around with
[EmberJS](http://www.emberjs.com), but decided this is also not quite suited for a blog (I don't remember which article
pointed this out; but blogs are mostly about sporadic users viewing one or two of your posts, why have them download
a whole bunch of JS?). Besides, I get a lot of EmberJS playing time at my job at [SRXP](http://www.srxp.com) these days.
So instead I took an entirely different approach:

- I like having everything in repos; so why couldn't my blog be a repo? Step 1: create Git-repo for blog.
- Posts are just text files in the repo; every post consists of a config file (in JSON, 'cause every programming
  language can read it easily) and a content source. I can write them in Markdown, or in HTML if I need something fancy.
   But oh no, what if I want to create a post while on the road without access to my own computer (read: private key
  for checking out the repo)? Solution: put the entire thing on GitHub, which supports sweet inline-editing
  of the repository.
- Screw managing and storing content yourself: I already used YouTube for videos; now I'll use SoundCloud for sounds,
  and whatever-box for whatever may come up in the future. There's a better solution for everything than the one I
  have the time to come up with.
- A Rakefile takes the sources and turns them into a blog, neat, fast and static. Comments were spam-only until now,
  so these are out. I can always add Disqus or Facebook Comments later, no biggy. I've been wanting to use this
  Rake-thingy for a while now; seems everyone is using it these days. The only experience I have with Ruby was in
  my first year of Computer Science, and I recall we did not get along well. Ruby is really popular though, so maybe
  we got off on the wrong foot and it deserves another chance.