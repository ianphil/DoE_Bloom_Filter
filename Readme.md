Bloom filters are a great tool for us to focus on how to design an experiment that would be stitistcally sound.
I'm going to use the process of DoE, but first will will do a hack job.
There is a mathematically way to test each hypothesis so we ahve the answer key going in!
Let's see if we can desin experment to solve.

Get name files: git url (ref: url of other location)
Create usernames from name list: url of script
create data for study present/absent urls

We'll start with size: url to file
`size=10000` is where we start because that is the amount of names we have
we get a very high FP rate, adjust the size var again by doubling it and the % does go down. But this code is not testable. If we stopped there we would assume our Hypothisis was right. We need to create a test harness that can change that var... And when we do we get interesting results. While it does decrease it's not linear... hmm.

now lets say I want to duplicate this work for another factor. keeping size the same let's see what the amount of hash passes do to the FP. I'm not going to even wory about it... It should actually increase till the bits are full and then everything is just an FP. (I'm not absolutly sure of this...)

What have we learned? Increasing the size of bitarray decreases the FP. Increasing the hash passes increase the FP with deminishhing returns. While these conclusions are useful, they are not statistically relevent and no relationship between the factors can be deduced. This is where a well designed experiment would be helpful.

