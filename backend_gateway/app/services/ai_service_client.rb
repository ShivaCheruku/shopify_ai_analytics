class AiServiceClient
  include HTTParty
  base_uri ENV.fetch('AI_SERVICE_URL', 'http://localhost:8000')

  def self.process_question(store_id, question, access_token)
    post('/process', 
      body: { 
        store_id: store_id, 
        question: question, 
        access_token: access_token 
      }.to_json,
      headers: { 'Content-Type' => 'application/json' }
    )
  end
end
