function current_selections() {
    filters =[
       "running",
       "toggle_all",
       "Adjective",
       "Adverb",
       "Conjunction",
       "Idiom",
       "Interjection",
       "Noun",
       "Number",
       "Preposition",
       "Pronoun",
       "Verb",
       "CONJUNCTION_Verb_1",
       "CONJUNCTION_Verb_2",
       "CONJUNCTION_Verb_3",
       "CONJUNCTION_Verb_4",
       "CONJUNCTION_Verb_99", // irregular
       "STOPWORD_Verb_0", // stopword verb 
       "CONJUNCTION",
       "DECLENSION",
       "PROPER",
       "REGULAR",
       "STOPWORD",
       "PRINCIPAL_PARTS_NO_DIACRITICALS",
       "PRINCIPAL_PARTS",
       "SHORT_DEFINITION",
       "LONG_DEFINITION",
       "SIMPLE_LEMMA",
       "PART_OF_SPEECH",
       "LOGEION_LINK",
       "FORCELLINI_LINK",
       "Total_Count_in_Text",
       "Count_in_Selection",
       "Order_of_Appearance",
       "Source_Text"
    ]
    
    let result = '{'
    for (i = 0; i < filters.length -1; i++) {
        
        let filter = "#" + filters[i]
        let value = $(filter).val();
        console.log(filter, value);
        result +=  '"'+filters[i] + '":"' + value + '",'
        console.log(result);
    }
    let filter = "#" + filters[filters.length-1] 
    let value = $(filter).val();
    result += '"' + filters[filters.length-1] + '":"' + value + '"}';
    return JSON.parse(result);
};

