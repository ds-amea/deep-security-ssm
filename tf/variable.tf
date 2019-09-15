variable "AWS_ACCESS_KEY" {}
variable "AWS_SECRET_KEY" {}
variable "AWS_REGION" {
}

variable "EC2_tag_key" {
  description = "Enter EC2 Tag Key that has to be searched for installing agent:"
}

variable "EC2_tag_value" {
  description = "Enter EC2 Tag Value that has to be searched for installing agent:"
}

variable "DSM_URL" {
  description = "Enter Deep Security manager URL for Dashboard:"
}

variable "DSA_URL" {
  description = "Enter Deep Security agent activation:"
}

variable "DSA_Activation_Port" {
  description = "Enter Deep Security agent activation port(default 443):"
}

variable "DSM_Tenent_ID" {
  description = "Enter Deep Security tenet ID (Required):"
}

variable "Tenent_Token" {
  description = "Enter Deep Security Token for tenent(Required):"
}

variable "Default_policyNo_windows" {
  description = "Enter Default Linux policy no (default 1):"
}

variable "Default_policyNo_linux" {
  description = "Enter Default Windows policy no (default 1):"
}
