class UrlMappings {

	static mappings = {
        "/api/circle" {
            controller = 'circle'
            action = [POST: 'point']
        }
	}
}
