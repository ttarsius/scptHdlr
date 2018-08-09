#交换机、MSE、SR设备对应的数据表结构（第一版）

CREATE TABLE nhsjwg_device(
  id           INT NOT NULL AUTO_INCREMENT,
  NMS          VARCHAR(100) NOT NULL,
  alias        VARCHAR(100) NOT NULL,
  IP           VARCHAR(50)  NOT NULL,
  section      VARCHAR(20)  NOT NULL,
  factory      VARCHAR(50)  NOT NULL,
  device_type  VARCHAR(50)  NOT NULL,
  PRIMARY KEY (id)
) CHARSET=utf8mb4;