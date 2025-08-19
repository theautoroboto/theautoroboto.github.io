/**
 * Array containing work excuses.
 */
var EXCUSES = [
    "I just found out my former mother-in-law passed away. She was on her fourth bout with cancer, and she lost her balance and fell off a huge hill by their house today. I’m not sure when her funeral will be, but I will keep everyone posted.",
    "I have a stomach virus.",
    "I have a doctor's appointment.",
    "I have to pick my son up from summer camp.",
    "My car's starter is out.",
    "My car will not start.",
    "The tow truck is late.",
    "I need to take my kid to court.",
    "I need to take my kid to practice.",
    "I need to take my kid to the ortho.",
    "I have a basketball tournament.",
    "I have a family issue.",
    "I'm taking my son to get a physical.",
    "I bruised my ribs.",
    "My kid lost their retainer.",
    "I strained my back.",
    "My son's high school received a gun threat.",
    "I'm still getting over a stomach virus.",
    "I got a call to pick up my kid from school.",
    "I need to get my kid off the bus today.",
    "My youngest is running a fever and is congested.",
    "A side of beef is being delivered this afternoon.",
    "Our cable and Wi-Fi went down last night.",
    "My son is getting fitted for his retainer.",
    "I had to take my son in for a cut on his finger this morning.",
    "I spilled coffee all over myself at the gas station this morning.",
    "I have to take my son to an eye appointment.",
    "My son is sick.",
    "I'm pretty sure I won't last the day with this poison oak.",
    "I'm dropping my son off at basketball conditioning.",
    "I need to take my son to the Chris Spielman football camp.",
    "I have a doctor's appointment this morning.",
    "My oldest has basketball. My middle son is working with his grandfather, so I'm the only one here.",
    "I'm going to the dentist.",
    "I'm dropping my son off at his grandparents'.",
    "I'm taking the team to lunch today, and we are buying supplies for the walking taco event this Friday. I need to take stuff back to my house to refrigerate.",
    "It turns out I have poison oak on my legs, so I'm going to work from home today so I can air them out.",
    "I'm helping out with the neighbor this morning.",
    "My oldest son's ride for basketball camp was canceled this morning.",
    "I'm helping the neighbor.",
    "I'm taking the kids to their dentist appointment.",
    "We have a realtor coming over and another guy about the carpet. We're trying to sell and buy a new house.",
    "I have a guy stopping by to give us an estimate on repairing our driveway.",
    "I'm helping family set up for my niece's graduation.",
    "My father needs some help with some heavy lifting.",
    "I have shingles.",
    "I'm waiting for my son to get back home from Cleveland.",
    "I'm dropping my kid off to help their grandparents.",
    "I need to take my son to Cleveland.",
    "While I was at the store, our neighbor (who's going through chemo) passed out, so we had to call an ambulance for her. Her husband passed away a little over a year ago, and she doesn't have any family close by, so we're heading to the hospital to be with her.",
    "I'm going to run to the store to get my neighbor some groceries.",
    "I'm keeping our neighbor's son with me until his grandpa picks him up.",
    "My neighbor, who has breast cancer, was just beaten up by her adopted daughter, who has autism.",
    "One of my kids threw up at school.",
    "I'm dropping my wife's vehicle off for routine maintenance.",
    "I have to go get my youngest a refill on his cough medicine.",
    "I had to clean up dog puke out of my car.",
    "I have to pick my middle one up from detention.",
    "My dog is sick.",
    "I need to work from home today so I can run to the facilities as needed.",
    "My stomach is upset this morning, so I'm running behind.",
    "I have a meeting with my youngest son's teacher at 8:30 am, and I need to leave around 2 pm to take my middle son to the orthodontist.",
    "I just went outside to leave, and my tire is completely flat now. Apparently, the plug didn't hold.",
    "We close on our new house today.",
    "I need to get a few things done around our house.",
    "I have to pick up my son; he'll be shadowing a kid at his soon-to-be new school for the day.",
    "The carpet guys are coming tomorrow.",
    "I have a funeral to attend.",
    "I'm taking my son to his follow-up doctor appointment for when he had his adenoids out.",
    "I'm still waiting for the guy to show up; he got hung up at his earlier job.",
    "The driveway guys are fixing our driveway today, and I'll be working on re-grouting the kitchen.",
    "We're having our carpet replaced.",
    "Our realtor is coming over this afternoon. I'm going to run home around noon to clean up a couple of things.",
    "My son is having surgery to have his adenoids removed... Hopefully, this will help with him getting sick.",
    "I just got a text for a house viewing today.",
    "I have to keep the dogs with me while they show the house.",
    "My son has a fever.",
    "I got something in my eye yesterday, and I can't get it out. I'm going to my eye doctor at 9 am this morning to have it removed. I'm not sure if and when I'll be in yet.",
    "I'm going to get lunch with my neighbor, and I should be in the office around noon.",
    "I'm still not feeling well.",
    "I'm sick to my stomach and need to use a sick day.",
    "My son still has a fever.",
    "Our pilot light went out on our hot water tank, and I can't get it to come back on. My neighbor is going to stop by.",
    "I'm having an allergic reaction to the medicine.",
    "I'm still sick, so I'm giving in and going to see the doctor today.",
    "I was literally walking out the door to come back to work, and here comes the realtor strolling up with his client for the showing.",
    "I have to pick up my sick kid from school.",
    "The school canceled the freshman boys' basketball game tonight and is moving the JV game so they can avoid the weather. I will be heading out so I can get there in time to do the scorebook.",
    "I'm still waiting on the bus to get here, then I have to run an errand.",
    "I'm dropping off a fruit salad.",
    "We're having issues with our furnace; I think our blower motor burned out. I'm going to start out from home today and call a few places to see if I can get someone out here today or just buy a motor. I may come in depending on what I find out.",
    "There's nothing like walking outside to see your new tire is going flat. I'm going to put some air in my tire and go get it patched (there's a screw in it).",
    "I have to pick my middle one up from detention.",
    "The HVAC technician replaced the capacitor ('flux,' I'm guessing) today, which fixed the issue temporarily, but they said to be prepared for the blower to go out, which it did. They ordered me a new one that will be here tomorrow, so I have to be home when they get here.",
    "I have a meeting with my youngest son's teacher.",
    "I got something in my eye yesterday, and I can't get it out.",
    "My son has tutoring, and then I'm taking him to McDonald's for breakfast.",
    "Our pilot light went out on our hot water tank, and I can't get it to come back on...",
    "We're having issues with our furnace.",
    "I'm picking my youngest up from school to take him to get some new pants.",
    "I need to run an errand.",
    "My son needs a ride to basketball practice, so I need to leave.",
    "I'm helping carry in food for a party.",
    "It turns out I have bronchitis.",
    "I will take my son to the doctor's today, and he has a dentist appointment and tutoring tomorrow.",
    "I have a house showing.",
    "The carpet guys didn't get finished today, so they'll finish up tomorrow.",
    "I have a few things going on here at home.",
    "I'm still not feeling well.",
    "I'm sick to my stomach.",
    "I need to take my dog to the vet. She fell going up our stairs last night, and this morning she's dragging her back leg, not limping but dragging.",
    "I'm dropping my sister-in-law off at the airport.",
    "My new tire is going flat.",
    "I had half a tooth come out a couple of hours ago, leaving the nerve completely exposed, so now I'm in a lot of pain.",
    "My son needs a ride to basketball practice."
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
