/**
 * Array containing work excuses.
 */
var EXCUSES = [
    "I just found out my former mother in law passed away. She was on her 4th bout with cancer & she lost her balance and fell off a huge hill by their house today. I’m not sure when her funeral will be yet but I will keep everyone posted.",
    "I have stomach virus",
"I have a doctor's appointment",
"Have to pick my son up from summer camp",
"Car's Starter Out",
"Car will not start",
"Tow Truck Late",
"Need to take kid to court",
"Take my kid to practice",
"Take my kid to Ortho",
"I have a basketball tournament",
"Family issue",
"Taking son to get a physical",
"Bruised my ribs",
"Kid lost retainer",
"Strained back",
"Son's high school received a gun threat",
"Still getting over a stomach virus",
"Got a call to pick up kid from school",
"need to get my kid off the bus today",
"youngest is running a fever and is congested",
"side of beef being delivered this afternoon",
"Our cable and wifi went down last night",
"son is getting fitted for his retainer",
"Had to take my son in for a cut on his finger this morning",
"I spilled coffee all over myself while at the gas station this morning",
"take son to Eye appointment",
"my son is sick",
"Pretty sure I won't last the day with this poison oak",
"dropping my son off at basketball conditioning",
"Need to take my son to the Chris Spielman football camp",
"I have a doctor Appointment this morning",
"My oldest has basketball. My middle son is working with his grandfather so I'm the only one here.",
"Going to Dentist",
"Dropping my son off to his grandparents",
"I'm taking the team to lunch today and we are buying supplies for the walking taco event this Friday. I need to take stuff back to my house to refrigerate",
"Turns out I have poison oak on my legs so I'm going to work from home today so I can air them out.",
"Helping out with the neighbor this morning",
"My oldest son's ride for basketball camp cancelled this morning ",
"helping the neighbor",
"taking kids to dentist appointment",
"We have a realtor coming over and another guy about carpet. Trying to sell and buy a new house.",
"I have a guy stopping by to give us an estimate on repairing our driveway",
"helping family set up for my niece's graduation",
"Father needs some help with some heavy lifting",
"shingles",
"Waiting for my son to get back home from Cleveland",
"Dropping kid off to help grandparents ",
"Need to take Son to Cleveland",
"While I was at the store our neighbor (who's going thru chemo) passed out so we just had to call the ambulance for her. Her husband passed away a little over a year ago and she doesn't have any family close by so we're heading to the hospital to be with her",
"Going to run to the store to get my neighbor some groceries",
"keeping our neighbor's son with me until his Grandpa picks him up",
"My neighbor who has breast cancer just got beat up by her adopted daughter who has autism",
"One of my kids threw up at school ",
"Dropping wife's vehicle off for routine maintenance",
"I have to go get my youngest a re-fill on his cough medicine",
"I had to clean up dog puke out of my car",
"I have to pick my middle one up from detention",
"Sick Dog",
"I need to work from home today so I can run to the facilities as needed.",
"My stomach is upset this morning so I'm running behind",
"I have a meeting with my youngest son's teacher at 8:30 am and I need to leave around 2pm to take my middle son to the orthodontist",
"Just went outside to leave and my tire is completely flat now. Apparently plug didn't hold",
"We close on our new house",
"Need to get a few things done around our house",
"pick up my son, he'll be shadowing a kid at his soon to be new school for the day",
"the carpet guys are coming tomorrow",
"Funeral",
"I'm taking my son to his follow up doctor appointment for when he had his adenoids out at ",
"Still waiting for guy to show up, he got hung up at his earlier job.",
"The driveway guys are fixing our driveway today and I'll be working on re-grouting the kitchen",
"We're having our carpet replaced",
"Our realtor is coming over this afternoon. I'm going to run home around noon to clean up a couple things",
"My son will is having surgery to have his adnoids removed... Hopefully this will help with him getting sick",
"Just got a text for a house viewing today",
"I have to keep the dogs with me while they show the house",
"Son has fever",
"I got something in my eye yesterday and I can't get it out. I'm going to my eye doctor at 9am this morning to have it removed. Not sure if and when I'll be in yet",
"I'm going to get lunch with my neighbor and I should be in the office around noon",
"Still not feeling well",
"I'm sick to my stomach, need to use a sick day",
"Son still has fever",
"Our pilot went out on our hot water tank and I can't get it to come back on. My neighbor is going to stop by ",
"allergic reaction to the medicine",
"I'm still sick so I'm giving in and going to see the doctor today.",
"I was literally walking out the door to come back in to work and here comes the realtor strolling up with his client for the showing",
"Pick up sick kid",
"School cancelled the freshman boys basketball game tonight and are moving the JV game so they can avoid the weather. I will be heading out so I can get there in time to do scorebook.",
"Still waiting on bus to get here, then I have to run an errand",
"dropping off fruit salad",
"We're having issues with our furnance, I think our blower motor burnt up. I'm going to start out from home today and call a few places to see if I can someone out here today or just buy a motor. I may come in depending on what I find out.",
"Nothing like walking outside to see your new tire is going flat. I'm going to put some air in my tire and go get it patched (there's a screw in it).",
"pick my middle one up from detention ",
"HVAC replaced the capacitor ('flux' I'm guessing) today which fixed the issue temporarily but but said be prepared for the blower to go out which it did. They ordered me a new one that will be here tomorrow so I have to be home when they get here.",
"meeting with my youngest son's teacher ",
"I got something in my eye yesterday and I can't get it out",
"My son has tutoring and then I'm taking him to McDonalds for breakfast",
"Our pilot went out on our hot water tank and I can't get it to come back on... ",
"We're having issues with our furnace",
"picking my youngest up from school to take to get some new  pants ",
"need to run an errand",
"My son needs a ride to basketball practice so I need to leave",
"Helping carry in food for a party ",
"Turns out I have Bronchitis",
"I will take my son to the doctor's today and he has a dentist appointment and tutoring tomorrow",
"I have a house showing",
"Carpet guys didn't get finished today so they'll finish up tomorrow",
"I have a few things going on here at home",
"Still not feeling well",
"I'm sick to my stomach",
"I need to take my dog to the vet. She fell down going up our stairs last night and this morning she's dragging her back leg. not limping but dragging",
"I'm dropping my sister in-law off at the airport",
"New tire is going flat ",
"I had half a tooth come out a couple hours ago leaving the nerve completely exposed so now I'm in a lot of pain.",
"son needs a ride to basketball practice"
];

const excuseContainer = document.getElementById('quote-container');
const excuseText = document.getElementById('quote');
const twitterBtn = document.getElementById('twitter');
const newQuoteBtn = document.getElementById('new-quote');

// Get Excuse from VAR
async function getExcuse() {
    try {
        var excuseIndex = Math.floor(Math.random() * EXCUSES.length);
        var excuse = EXCUSES[excuseIndex];
        // console.log(excuse);

        // Reduce long excuses
        // if (excuseText.length > 50){
        //     excuseText.classList.add('long-quote');
        // }
        // else {
        //     excuseText.classList.remove('long-quote');
        // }
        excuseText.innerText = excuse;

    }
    catch (error) {
        console.log('oopsie, no excuse', error);
    }
}

newQuoteBtn.addEventListener('click', getExcuse);


// On Load
getExcuse();
