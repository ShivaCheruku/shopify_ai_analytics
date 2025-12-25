module Api
  module V1
    class QuestionsController < ActionController::API
      def create
        store_id = params[:store_id]
        question = params[:question]

        if store_id.blank? || question.blank?
          render json: { error: 'store_id and question are required' }, status: :bad_request
          return
        end

        # In a real app, we'd fetch the store's access token from the DB
        # sessions = ShopifyApp::SessionRepository.retrieve_by_shop_name(store_id)
        mock_access_token = "shpua_mock_token_12345"

        result = AiServiceClient.process_question(store_id, question, mock_access_token)

        if result.success?
          render json: result.parsed_response
        else
          render json: { error: 'Failed to process question', details: result.body }, status: :internal_server_error
        end
      end
    end
  end
end
