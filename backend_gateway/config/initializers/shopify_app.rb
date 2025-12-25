ShopifyApp.configure do |config|
  config.application_name = "Shopify AI Analytics"
  config.old_secret = ""
  config.api_key = ENV.fetch('SHOPIFY_API_KEY', '')
  config.secret = ENV.fetch('SHOPIFY_API_SECRET', '')
  config.scope = "read_products,read_orders,read_inventory"
  config.embedded_app = true
  config.after_authenticate_job = false
  config.api_version = "2024-01"
  config.shop_session_repository = 'ShopifyApp::InMemorySessionStore'
  config.reauth_on_access_scope_changes = true
end
