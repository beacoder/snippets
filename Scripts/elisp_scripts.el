;; This buffer is for notes you don't want to save, and for Lisp evaluation.
;; If you want to create a file, visit that file with C-x C-f,
;; then enter the text in that file's own buffer.

(/ 1000000.0 4)
125000

(- (* 6 (/ 16777216  4)) 6)
749994

------------------



xcb_1             : first fail access
-> : 0.f0000000.11110000.0.4 <-
-> : 6.f0000000.11110000.6.8 <-
-> : 25165818.f0000000.11110000.6.16777216 <-

------------------


;; create batch debug failing cycles files
(let ((filename "") 
      (path "/opt/hsm/src/execution_engine/TEST.hsm/devices/moscato_ddr3_validation_256sites_r1.0.0/error_simulation/sh_libs/")
      (basename "_march6n_1333-999_feat46_label1_all_fail_"))
  (dotimes (site 257)
    (if (> site 0)
	(progn
	  (dolist (pin '("DQ.00" "DQ.01" "DQ.02" "DQ.03" "DQ.04" "DQ.05" "DQ.06" "DQ.07" "DQS" "DQSn"))
	    (progn
	      (setq filename (concat path (number-to-string site) basename pin ".log"))
	      (delete-file filename)
	      (append-to-file "


xcb_1             : first fail access
-> : 0.f0000000.11110000.0.4 <-
-> : 6.f0000000.11110000.6.8 <-
-> : 749994.f0000000.11110000.6.500000 <-
-># : 1499994.f0000000.11110000.6.1000000 <-
-># : 25165818.f0000000.11110000.6.16777216 <-" nil filename)
	      )
	    )
	  )
      )
    )
  )

