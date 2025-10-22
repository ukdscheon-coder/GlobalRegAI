const SPREADSHEET_ID = "1vLMM7GC7oIMO5wImxC2E1iPhN4fbXZvj9PHBfo4F0Gw";
const SHEET_NAME = "출력결과";
// AIzaSyALqyELQq8Pjgd0Z0orW19AUw6uyxZ9U3s - This key is for demonstration and should be replaced.
const GEMINI_API_KEY = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');


/**
 * Web App의 기본 엔드포인트입니다.
 * GET 요청을 받으면 index.html 파일을 서비스합니다.
 */
function doGet() {
  return HtmlService.createTemplateFromFile('index')
      .evaluate()
      .setTitle('GlobalRegAI')
      .addMetaTag('viewport', 'width=device-width, initial-scale=1.0');
}

/**
 * HTML 템플릿에 다른 HTML 파일을 포함시키기 위한 함수입니다.
 * @param {string} filename - 포함할 HTML 파일의 이름.
 * @return {string} 해당 파일의 HTML 콘텐츠.
 */
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

/**
 * 프론트엔드에서 호출하여 AI 프로젝트 계획을 생성하는 메인 함수입니다.
 * @param {object} formData - 사용자가 웹 앱에서 입력한 폼 데이터 객체.
 * @return {object} AI가 생성한 결과 및 성공 여부를 담은 객체.
 */
function generateProjectPlan(formData) {
  try {
    const prompt = createPrompt(formData);
    const geminiResponse = callGeminiAPI(prompt);
    const parsedResponse = JSON.parse(geminiResponse);

    saveToSheet(formData, parsedResponse);

    return { success: true, data: parsedResponse };
  } catch (error) {
    Logger.log("Error in generateProjectPlan: " + error.toString());
    return { success: false, message: error.toString() };
  }
}

/**
 * 프로젝트 히스토리 데이터를 구글 시트에서 가져옵니다.
 * @return {Array<Array<string>>} 시트의 데이터 배열.
 */
function getProjectHistory() {
  try {
    const sheet = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName(SHEET_NAME);
    const data = sheet.getDataRange().getValues();
    // 헤더를 제외하고 최신순으로 정렬하여 반환
    return data.slice(1).reverse();
  } catch (error) {
    Logger.log("Error in getProjectHistory: " + error.toString());
    return [];
  }
}


/**
 * Gemini API에 전달할 프롬프트를 생성합니다.
 * @param {object} data - 사용자 입력 데이터.
 * @return {string} 완성된 프롬프트 문자열.
 */
function createPrompt(data) {
  // 사용자의 입력을 기반으로 AI에게 역할을 부여하고 구체적인 지시를 내립니다.
  // JSON 형식으로 출력을 요청하여 파싱하기 용이하게 만듭니다.
  return `
    You are a world-class global regulatory affairs expert specializing in medical devices, pharmaceuticals, and cosmetics. Your name is "RegAI".
    Based on the following user requirements, create a detailed and actionable regulatory strategy and project timeline.

    **User Requirements:**
    - Target Country: ${data.country}
    - Product Type: ${data.productType}
    - Regulatory Class: ${data.regulatoryClass}
    - Budget Scale: ${data.budget}
    - Additional Options: ${data.advancedOptions.join(', ') || 'None'}

    **Your Task:**
    Generate a response in a strict JSON format. Do not include any text outside of the JSON structure.
    The JSON object must contain the following keys:
    1.  "recommendedPath": A string describing the optimal regulatory pathway. (e.g., "Korea MFDS Class II -> EU MDR Class IIa -> US FDA 510(k)")
    2.  "estimatedDuration": A string for the total estimated project duration. (e.g., "18-24 months")
    3.  "estimatedCost": A string for the estimated cost. (e.g., "200-300 million KRW")
    4.  "detailedSchedule": An array of objects, where each object represents a phase with "phaseName" (e.g., "Phase 1: Preparation (0-3 months)") and "tasks" (an array of strings, e.g., "2025-11-01: Gap analysis and document review").
    5.  "keyDeadlines": An array of objects, where each object has "date" and "description" for critical deadlines. (e.g., {"date": "2026-02-02", "description": "QMSR transition deadline"})
    6. "aiPath": A concise summary string of the recommended path for spreadsheet logging.

    Example of a task in detailedSchedule: "YYYY-MM-DD: Task description".
    Ensure the timeline and recommendations are realistic and professional.
    `;
}

/**
 * Google AI Gemini 모델을 호출합니다.
 * @param {string} prompt - AI에게 보낼 프롬프트.
 * @return {string} AI 모델의 텍스트 응답.
 */
function callGeminiAPI(prompt) {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_API_KEY}`;

  const payload = {
    "contents": [{
      "parts": [{
        "text": prompt
      }]
    }],
    "generationConfig": {
      "responseMimeType": "application/json",
      "temperature": 0.4,
      "topP": 1,
      "topK": 32,
      "maxOutputTokens": 8192,
    }
  };

  const options = {
    'method': 'post',
    'contentType': 'application/json',
    'payload': JSON.stringify(payload),
    'muteHttpExceptions': true
  };

  const response = UrlFetchApp.fetch(url, options);
  const responseText = response.getContentText();
  const responseCode = response.getResponseCode();

  if (responseCode !== 200) {
    throw new Error(`Gemini API Error: ${responseCode} - ${responseText}`);
  }

  const jsonResponse = JSON.parse(responseText);
  // Gemini API 응답 구조에 따라 실제 텍스트 부분만 추출
  return jsonResponse.candidates[0].content.parts[0].text;
}

/**
 * 분석 결과를 구글 시트에 저장합니다.
 * @param {object} formData - 사용자 입력 데이터.
 * @param {object} aiResponse - AI가 생성한 파싱된 응답 데이터.
 */
function saveToSheet(formData, aiResponse) {
  const sheet = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName(SHEET_NAME);
  const timestamp = new Date();
  const user = Session.getActiveUser().getEmail() || 'Unknown';

  // 시트의 헤더 순서와 정확히 일치해야 합니다.
  const newRow = [
    generateProjectId(), // 프로젝트_ID
    timestamp,           // 기록일시
    user,                // 사용자
    formData.country,    // 국가
    formData.productType,// 제품종류
    formData.regulatoryClass, // 인허가등급
    formData.budget,     // 예산규모
    aiResponse.aiPath,   // AI추천경로 (요약)
    JSON.stringify(aiResponse.detailedSchedule, null, 2), // 상세일정 (JSON 문자열로 저장)
    '시작전',           // 진행상태 (초기값)
    '',                  // 담당자 (초기값)
    ''                   // 비고 (초기값)
  ];

  sheet.appendRow(newRow);
}

/**
 * 간단한 고유 프로젝트 ID를 생성합니다.
 * @return {string} 'GR' + 현재 타임스탬프 기반의 ID.
 */
function generateProjectId() {
  return 'GR' + new Date().getTime().toString().slice(-6);
}
