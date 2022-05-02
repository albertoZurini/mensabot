use teloxide::prelude::*;
use scraper::{Html, Selector};
use rustc_serialize::json::Json;
use std::fs::File;
use std::io::Read;


fn add_emoticon(text : String) -> String {
    if text.contains("Sweets") {
        format!("{}🧁🧁", text)
    } else {
        text
    }
}

fn print_type_of<T>(_: &T) {
    println!("{}", std::any::type_name::<T>())
}


#[tokio::main]
pub async fn main() -> Result<(), reqwest::Error> {
    pretty_env_logger::init();
    log::info!("Starting bot...");

    let mut file = File::open("credentials.json").unwrap();
    let mut data = String::new();
    file.read_to_string(&mut data).unwrap();

    let json  = Json::from_str(&data).unwrap();

    let bot_token : &str = json.find_path(&["bot_token"]).unwrap().as_string().unwrap();

    let chat_ids = json.find_path(&["broadcast_chats"]).unwrap().as_array().unwrap(); //teloxide::types::ChatId(); // TODO: array
    let debug_id = teloxide::types::ChatId(json.find_path(&["debug_chat_id"]).unwrap().as_i64().unwrap());
    let api_endpoint = json.find_path(&["endpoint_url"]).unwrap().as_string().unwrap();

    let mut resp = reqwest::get(api_endpoint).await?;
    let body = resp.text().await?;
    let fragment = Html::parse_fragment(&body);

    let mut selectors = Vec::new();
    // identifier, translated name, order
    selectors.push(("Menü I\n", "Menu 1", 0));
    selectors.push(("Menü II\n", "Menu 2", 1));
    selectors.push(("Grillgericht", "Grill", 2));
    selectors.push(("Vitalgericht", "Vital dish", 3));
    selectors.push(("Fastlane", "Fastlane", 4));
    selectors.push(("Nachtmenü", "Night", 5));

    let mut output : Vec<String> = Vec::new();
    output.push("".to_string());output.push("".to_string());output.push("".to_string());output.push("".to_string());output.push("".to_string());output.push("".to_string());

    let all_menus_selectors = &Selector::parse(".singleDay:nth-child(1) .dishWrapper").unwrap();
    let all_menus_html = fragment.select(all_menus_selectors);

    for menu_html in all_menus_html {
        for (name, translated_name, index) in &selectors {
            let menu_type_selector = Selector::parse(".headline").unwrap();
            let menu_type_text = menu_html.select(&menu_type_selector).next().unwrap().text().collect::<String>();
            let menu_selector = Selector::parse(".description .language02").unwrap();
            let menu_text = menu_html.select(&menu_selector).next().unwrap().text().collect::<String>().trim().to_owned();
            
            if menu_type_text.contains(name) {
                let text_wip = format!("{}\n\n{}\n\n", translated_name, add_emoticon(menu_text));
                output[(*index) as usize] = text_wip;
                break;
            }
        }
    }
    let mut message_text : String = "".to_owned();
    for menu_string in output {
        message_text.push_str(&menu_string);
    }

    let bot = Bot::new(bot_token); // ::from_env()
    for chat_id in chat_ids {
        let chat_id_teloxide = teloxide::types::ChatId(chat_id.as_i64().unwrap());

        bot.send_message(chat_id_teloxide, &message_text).send().await.unwrap();
    }
    Ok(())
}
