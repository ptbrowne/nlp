// Set up a collection to contain lyric information. On the server,
// it is backed by a MongoDB collection named "lyrics."

//Lyrics = new Meteor.Collection("lyrics_letsingit");
Lyrics = new Meteor.Collection("lyrics_letsingit_meteor");

if (Meteor.is_client) {

  Template.leaderboard.lyrics = function () {
    var n = 0;
    return Lyrics.find({"title":{"$exists":true}}, {sort: {genre: 1, title: 1}}).map(function (lyric) { 
        n = n+1;
        a = lyric
        a.lyrics = _.map(a.lyrics, function(p) {
            return p.split("\n");
        });
        a.n = n;
        return a
     });
  };

  Template.leaderboard.number_song_tagged = function () {
    return "" + Lyrics.find({
        tags : {$exists : true, $ne: []}					
    }).count()
  }
  
  Template.leaderboard.number_song = function() {
    return "" + Lyrics.find({title: {$exists : true}}).count()
  }
  Template.leaderboard.selected_name = function () {
    var lyric = Lyrics.findOne(Session.get("selected_lyric"));
    return lyric && lyric.title;
  };
  
  Template.leaderboard.tags = function () {
    return Lyrics.find({tag:{"$exists": true}}, {sort:{tag:1}}).map(function(tag) {
        tag.n = Lyrics.find({tags : tag.tag}).count()
        return tag
    })
  };
  
  Template.lyric.selected = function () {
    return Session.equals("selected_lyric", this._id) ? "selected" : '';
  };

  Template.leaderboard.events = {
    'keyup #addTag': function (evt) {
      if (evt.type === "keyup" && evt.which === 13) {
          new_tag = $("#addTag").attr("value");
          if (Lyrics.find({tag:new_tag}).count() == 0)
            Lyrics.insert({tag: new_tag});
          $("#addTag").attr("value", "");
        }
    }
  };

  Template.lyric.events = {
    'click span.name': function () {
        console.log("coucou");
      Session.set("selected_lyric", this._id);
      var lyric = Lyrics.findOne(Session.get("selected_lyric"));
    },
    'click span.tag' : function(evt) {
        tag = evt.srcElement.innerHTML;
        Lyrics.update(this._id, { $pull : { tags : tag } });
    }
    
  };
  
  Template.tag.events = {
    'click .name' : function () {
        console.log(Lyrics.update(Session.get("selected_lyric"), {$addToSet: {tags:this.tag}}));
    },
    'click .del': function(evt) {
        if (confirm("if you remove this tag, it will be removed from all the songs, you sure ?")) {
            Lyrics.update({tags : this.tag}, 
                          {$pull : {tags:this.tag}},
                          {multi: true});
            Lyrics.remove(this._id);
        }
    }
  }
}

// On server startup, create some lyrics if the database is empty.
if (Meteor.is_server) {
  Meteor.startup(function () {
//    Lyrics.find({}).forEach(function(item) {
//        delete item._id;
//        mLyrics.insert(item);
//    })
  
    if (Lyrics.find({tag:{"$exists":true}}).count() === 0) {
      var tags = ["love",
                   "war",
                   "protest",
                   "jealousy",
                   "party",
                   "drugs",
                   "despair",
                   "devil"];
      for (var i = 0; i < tags.length; i++) 
        Lyrics.insert({tag: tags[i]});
    }
  });
}
