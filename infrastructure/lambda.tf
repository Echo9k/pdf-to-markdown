resource "aws_lambda_function" "pdf_to_markdown" {
  function_name = "pdf-to-markdown"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec.arn
  filename      = "${path.module}/../output/lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/../output/lambda.zip")
  timeout       = 60
  memory_size   = 512
  environment {
    variables = {
      # Add your env vars here
    }
  }
}